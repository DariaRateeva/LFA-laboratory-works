from ast_nodes import NumberNode
from ast_nodes import UnaryOpNode
from ast_nodes import BinaryOpNode
from ast_nodes import FunctionNode



# ast_printer.py

def print_ast(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + node_label(node))

    new_prefix = prefix + ("    " if is_last else "│   ")
    children = get_children(node)

    for i, child in enumerate(children):
        print_ast(child, new_prefix, i == len(children) - 1)

def node_label(node):
    if isinstance(node, NumberNode):
        return f"Number({node.value})"
    if isinstance(node, UnaryOpNode):
        return f"Unary({node.op_token.type})"
    if isinstance(node, BinaryOpNode):
        return f"Operation({node.op_token.type})"
    if isinstance(node, FunctionNode):
        return f"Function({node.func_token.type})"
    return "Unknown"

def get_children(node):
    if isinstance(node, NumberNode):
        return []
    if isinstance(node, UnaryOpNode):
        return [node.operand]
    if isinstance(node, BinaryOpNode):
        return [node.left, node.right]
    if isinstance(node, FunctionNode):
        return [node.argument]
    return []

