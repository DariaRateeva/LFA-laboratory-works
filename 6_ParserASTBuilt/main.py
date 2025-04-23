# main.py
from lexer import Lexer
from parser import Parser
from ast_printer import print_ast

def test_lexer(input_text):
    lexer = Lexer(input_text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == "EOF":
            break
    return tokens

if __name__ == "__main__":
    user_input = input("Enter a mathematical expression: ")
    tokens = test_lexer(user_input)

    print("\nTokenized Output:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("\nAST Tree:")
        print_ast(ast)
    except Exception as e:
        print(f"Parser error: {e}")
