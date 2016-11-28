# -*- coding: utf-8 -*-

"""
Functions for determining different features about ast nodes.
"""

from utils import *
from builtin_types import *

import ast

# AST primitives
PRIMITIVE_AST_NODES = (
    ast.Num,
    ast.Str,
    ast.Bytes,
)


"""
Feature extraction
"""


def determine_variable_type(node):
    """Determine the type of a variable node.

    Returns:
        str: The type as a string.
    """
    if node is None:
        # Nothing specified deafults to no return type
        return Type("void")
    elif isinstance(node, ast.Name):
        if node.id == "str":
            # Strings are represented as char pointers
            return Type("char*")
        else:
            return Type(node.id)
    elif isinstance(node, ast.List):
        # Lists are represented as pointers to whatever they contain
        return PointerType(determine_variable_type(node.elts[0]))
    else:
        raise RuntimeError("Unknown var type '{}'".format(node))


def determine_literal_type(expr):
    """Determine the type of a literal node."""
    if isinstance(expr, ast.Num):
        if isinstance(expr.n, int):
            return Type("int")
        elif isinstance(expr.n, float):
            return Type("float")
        else:
            raise RuntimeError("Unknown literal num type for {}".format(expr.n))
    elif isinstance(expr, ast.Str):
        return Type("char*")
    else:
        raise RuntimeError("Unknown literal type\n{}".format(prettyparsetext(expr)))


def determine_function_return_type(func, frame):
    """Determine the return type of a function and add it to the frame."""
    name = func.func.id
    if name not in frame:
        raise RuntimeError("Function '{}' was not declared beforehand.".format(name))
    return frame[name]


def determine_expr_type(expr, frame):
    """Determine the type of an expression and potentially add it to the frame."""
    if isinstance(expr, ast.Call):
        return determine_function_return_type(expr, frame)
    elif isinstance(expr, ast.UnaryOp):
        return determine_expr_type(expr.operand, frame)
    elif isinstance(expr, ast.BinOp):
        # TODO: Check the right hand side also
        return determine_expr_type(expr.left, frame)
    elif isinstance(expr, (ast.Compare, ast.BoolOp)):
        # All boolean expressions will default to int for now
        return Type("int")
    elif isinstance(expr, PRIMITIVE_AST_NODES):
        return determine_literal_type(expr)
    elif isinstance(expr, ast.Name):
        if expr.id not in frame:
            raise RuntimeError("Unable to find variable/function '{}' in frame: {}".format(expr.id, list(frame.keys())))
        return frame[expr.id]
    else:
        raise RuntimeError("Unable to determine type for expression type {}".format(expr))


def determine_format_specifier(expr, frame):
    """Determine the format specifier for an expression node.

    Returns:
        str: the format specifier
    """
    arg_type = determine_expr_type(expr, frame)
    if arg_type == "char*":
        return "%s"
    elif arg_type == "int":
        return "%d"
    elif arg_type == "float":
        return "%f"
    elif arg_type.num_types() > 1:
        # Calls a function that returns a string
        return "%s"
    else:
        raise RuntimeError("TODO: Implement way of determining format specifier for {}".format(expr))


