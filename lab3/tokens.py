# tokens.py

class TokenType:
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    EXPONENT = "EXPONENT"
    FACTORIAL = "FACTORIAL"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SIN = "SIN"
    COS = "COS"
    TAN = "TAN"
    LOG = "LOG"
    SQRT = "SQRT"
    EXP = "EXP"
    ABS = "ABS"
    POW = "POW"
    PI = "PI"
    E = "E"
    EOF = "EOF"
    INVALID = "INVALID"

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"
