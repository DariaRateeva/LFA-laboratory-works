# ast_nodes.py
class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op_token, operand):
        self.op_token = op_token
        self.operand = operand

class FunctionNode(ASTNode):
    def __init__(self, func_token, argument):
        self.func_token = func_token
        self.argument = argument


def print_ast(node, indent=""):
    if isinstance(node, NumberNode):
        print(indent + f"Number({node.value})")
    elif isinstance(node, UnaryOpNode):
        print(indent + f"Unary({node.op_token.type})")
        print_ast(node.operand, indent + "  ")
    elif isinstance(node, BinaryOpNode):
        print(indent + f"Operation({node.op_token.type})")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")
    elif isinstance(node, FunctionNode):
        print(indent + f"Function({node.func_token.type})")
        print_ast(node.argument, indent + "  ")
