# -*- coding: utf-8 -*-

"""
Functions for determining different features about ast nodes.
"""

from utils import *


"""
Types
"""


class Type(object):
    def __init__(self, name):
        self.__first_name = name
        self.__names = set([name])
        self.__reset_mult_type_name()

    def add_type(self, name):
        if name not in self.__names:
            if isinstance(name, str):
                self.__names.add(name)
                self.__mult_type_name += self.__var_name_abbreviation(name)
            else:
                self.__names |= name.names()
                self.__reset_mult_type_name()

    def __reset_mult_type_name(self):
        self.__mult_type_name = "mult_type_" + "".join(self.__var_name_abbreviation(n) for n in self.__names)

    def __var_name_abbreviation(self, name):
        """The struct representing the name of the type containing multiple
        types will be mult_type_ followed by the first characters of the
        contained types.

        Pointers will have the character follwed by the depth of the pointer.

        For example:
            [int] -> "int"
            [char*] -> "char*"
            [int, float] -> "mult_type_if" (or "mult_type_fi")
            [char*, char] -> "mult_type_c1c" (or "mult_type_cc1")
            [int, float, char**] -> "mult_type_ifc2" (or ...)
        """
        return name[0] + str(name.count("*"))

    def types(self):
        return self.__names

    def type_name(self):
        if len(self.__names) == 1:
            return self.__first_name
        else:
            return self.__multi_type_name

    def __str__(self):
        return self.type_name()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.type_name() == other
        elif isinstance(other, Type):
            return self.type_name() == other.type_name()
        else:
            raise NotImplementedError("Cannot compare Type with {}".format(type(other)))

    def __hash__(self):
        return hash(frozenset(self.__names))


class PointerType(Type):
    def __init__(self, t):
        super().__init__(str(t) + "*")



"""
Primitive data types
"""

class IntType(Type):
    def __init__(self):
        super().__init__("int")


class FloatType(Type):
    def __init__(self):
        super().__init__("float")


class VoidType(Type):
    def __init__(self):
        super().__init__("void")


class StrType(Type):
    def __init__(self):
        super().__init__("char*")


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
        return VoidType()
    elif isinstance(node, ast.Name):
        if node.id == "str":
            # Strings are represented as char pointers
            return StrType()
        else:
            return Type(node.id)
    elif isinstance(node, ast.List):
        # Lists are represented as pointers to whatever they contain
        #return determine_variable_type(node.elts[0]) + "*"
        return PointerType(determine_variable_type(node.elts[0]))
    else:
        raise RuntimeError("Unknown var type '{}'".format(node))


def determine_literal_type(expr):
    """Determine the type of a literal node."""
    if isinstance(expr, ast.Num):
        return IntType()
    elif isinstance(expr, ast.Str):
        return StrType()
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
    elif isinstance(expr, ast.Name):
        if expr.id not in frame:
            raise RuntimeError("Unable to find variable/function '{}' in frame: {}".format(expr.id, list(frame.keys())))
        return frame[expr.id]
    elif isinstance(expr, ast.UnaryOp):
        return determine_expr_type(expr.operand, frame)
    elif isinstance(expr, ast.BinOp):
        # TODO: Check the right hand side also
        return determine_expr_type(expr.left, frame)
    elif isinstance(expr, (ast.Compare, ast.BoolOp)):
        # All boolean expressions will default to int for now
        return IntType()
    else:
        return determine_literal_type(expr)


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
    else:
        raise RuntimeError("TODO: Implement way of determining format specifier for {}".format(expr))


