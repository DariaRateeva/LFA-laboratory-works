# parser.py
from ast_nodes import *
from tokens import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token().type == token_type:
            self.pos += 1
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token().type}")

    def parse(self):
        return self.expression()

    def factor(self):
        token = self.current_token()

        if token.type == TokenType.PLUS or token.type == TokenType.MINUS:
            self.eat(token.type)
            return UnaryOpNode(token, self.factor())

        if token.type == TokenType.INTEGER or token.type == TokenType.FLOAT:
            self.eat(token.type)
            return NumberNode(token.value)

        if token.type in (TokenType.SIN, TokenType.COS, TokenType.TAN, TokenType.LOG, TokenType.SQRT, TokenType.EXP, TokenType.ABS, TokenType.POW):
            self.eat(token.type)
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return FunctionNode(token, node)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        raise Exception(f"Unexpected token: {token}")

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.current_token()
            self.eat(token.type)
            node = BinaryOpNode(node, token, self.factor())
        return node

    def expression(self):
        node = self.term()
        while self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token()
            self.eat(token.type)
            node = BinaryOpNode(node, token, self.term())
        return node
