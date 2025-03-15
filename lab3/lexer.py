# lexer.py

import re
from tokens import TokenType, Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def advance(self):
        """Move to the next character."""
        self.pos += 1

    def peek(self):
        """Look at the next character without moving forward."""
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        return None

    def get_next_token(self):
        """Tokenize the input string."""
        while self.pos < len(self.text):
            char = self.text[self.pos]

            if char.isspace():  # Ignore whitespace
                self.advance()
                continue

            if char.isdigit() or char == '.':  # Handle numbers
                return self.number()

            if char.isalpha():  # Handle functions & constants
                return self.identifier()

            if char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if char == '%':
                self.advance()
                return Token(TokenType.MODULO, '%')

            if char == '^':
                self.advance()
                return Token(TokenType.EXPONENT, '^')

            if char == '!':
                self.advance()
                return Token(TokenType.FACTORIAL, '!')

            if char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            # If we get here, it's an invalid character
            self.advance()
            return Token(TokenType.INVALID, char)

        return Token(TokenType.EOF, None)  # End of input

    def number(self):
        """Recognizes integers and floating-point numbers."""
        num_str = ""
        is_float = False

        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            if self.text[self.pos] == '.':
                if is_float:  # Second decimal point is invalid
                    break
                is_float = True
            num_str += self.text[self.pos]
            self.advance()

        if is_float:
            return Token(TokenType.FLOAT, float(num_str))
        else:
            return Token(TokenType.INTEGER, int(num_str))

    def identifier(self):
        """Recognizes function names and constants."""
        ident = ""
        while self.pos < len(self.text) and self.text[self.pos].isalpha():
            ident += self.text[self.pos]
            self.advance()

        ident_lower = ident.lower()

        function_map = {
            "sin": TokenType.SIN,
            "cos": TokenType.COS,
            "tan": TokenType.TAN,
            "log": TokenType.LOG,
            "sqrt": TokenType.SQRT,
            "exp": TokenType.EXP,
            "abs": TokenType.ABS,
            "pow": TokenType.POW,
        }

        constant_map = {
            "pi": (TokenType.PI, 3.14159),
            "e": (TokenType.E, 2.71828),
        }

        if ident_lower in function_map:
            return Token(function_map[ident_lower], ident_lower)
        elif ident_lower in constant_map:
            return Token(constant_map[ident_lower][0], constant_map[ident_lower][1])
        else:
            return Token(TokenType.INVALID, ident)
