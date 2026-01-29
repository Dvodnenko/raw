import re

from ...domain import Spec, FieldSpec, And, Or, Not, InvalidValue


TOKEN_RE = re.compile(
    r"""
    \s*(
        \(|\)
        |and|or|not
        |eq|ne|gt|lt|gte|lte|like
        |[a-zA-Z_][a-zA-Z0-9_]*
        |'[^']*'
        |\S
    )
    """,
    re.VERBOSE
)

def tokenize(expr: str):
    return [t for t in TOKEN_RE.findall(expr) if t.strip()]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self) -> Spec:
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.peek() == "or":
            self.consume()
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.peek() == "and":
            self.consume()
            right = self.parse_not()
            left = And(left, right)
        return left

    def parse_not(self):
        if self.peek() == "not":
            self.consume()
            return Not(self.parse_atom())
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()

        if tok == "(":
            self.consume()
            expr = self.parse()
            if self.consume() != ")":
                raise InvalidValue("missing ')'")
            return expr

        field = self.consume()
        op = self.consume()
        value = self.consume()

        if value == "null":
            value = None
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]

        return FieldSpec(field, op, value)

def parse_infix(expr: str):
    tokens = tokenize(expr)
    parser = Parser(tokens)
    return parser.parse()
