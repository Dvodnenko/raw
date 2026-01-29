import re


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
