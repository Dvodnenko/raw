from dataclasses import dataclass

from ._parsers import akf_parser, AKF_TYPE_HINT


@dataclass
class Parsers:
    """
    All parsers take list of strings (from `sys.argv`) and return a `list` 
    with parsed arguments
    """

    parse_akf: AKF_TYPE_HINT = akf_parser
