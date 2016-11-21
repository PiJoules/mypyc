# -*- coding: utf-8 -*-

"""
Functions for converting nodes of the python ast to nodes of the c ast.
"""

import cgen
import ast


"""
Type extraction
"""


def determine_variable_type(node):
    """Determine the type of a variable node.

    Returns:
        str: The type as a string.
    """
    if node is None:
        # Nothing specified deafults to no return type
        return "void"
    elif isinstance(node, ast.Name):
        if node.id == "str":
            # Strings are represented as char pointers
            return "char*"
        else:
            return node.id
    elif isinstance(node, ast.List):
        # Lists are represented as pointers to whatever they contain
        return determine_variable_type(node.elts[0]) + "*"
    else:
        raise RuntimeError("Unknown var type '{}'".format(node))


def determine_literal_type(expr):
    """Determine the type of a literal node."""
    if isinstance(expr, ast.Num):
        return "int"
    elif isinstance(expr, ast.Str):
        return "char*"
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
        return frame[expr.id]
    else:
        return determine_literal_type(expr)


"""
Conversions
"""


def convert_variable_declaration(node, name):
    """Convert a python variable declaration to a c declaration."""
    return cgen.Value(determine_variable_type(node), name)


def convert_argument_declarations(args):
    """Convert a list of argument declarations to c argument declarations."""
    return [convert_variable_declaration(a.annotation, a.arg) for a in args.args]


def convert_operand(node):
    """Convert a binary operand to the corresponding valid c operation."""
    if isinstance(node, ast.Add):
        return "+"
    elif isinstance(node, ast.Sub):
        return "-"
    elif isinstance(node, ast.Mult):
        return "*"
    elif isinstance(node, (ast.Div, ast.FloorDiv)):
        return "/"
    elif isinstance(node, ast.Mod):
        return "%"
    elif isinstance(node, ast.Pow):
        raise RuntimeError("TODO: Implement power operations")
    elif isinstance(node, ast.LShift):
        return "<<"
    elif isinstance(node, ast.RShift):
        return ">>"
    elif isinstance(node, ast.BitOr):
        return "|"
    elif isinstance(node, ast.BitXor):
        return "^"
    elif isinstance(node, ast.BitAnd):
        return "&"
    elif isinstance(node, ast.MatMult):
        raise RuntimeError("TODO: Implement matrix multiplication operations")
    else:
        raise RuntimeError("Uknown binary operation {}".format(node))


def convert_expression(node):
    """Convert a python expression to the valid c code."""
    if isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Str):
        return "\"{}\"".format(node.s)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.BinOp):
        return convert_binary_operation(node)
    elif isinstance(node, ast.Call):
        return convert_call(node)
    else:
        raise RuntimeError("Unknown expression \n{}".format(prettyparsetext(node)))


def convert_binary_operation(node):
    """Convert a binary operation to the corresponding valid c code."""
    return "{} {} {}".format(
        convert_expression(node.left),
        convert_operand(node.op),
        convert_expression(node.right)
    )


def convert_call(node):
    """Convert a python function call to the valid c representation."""
    return "{name}({args})".format(
        name=convert_expression(node.func),
        args=", ".join(convert_expression(a) for a in node.args)
    )


def convert_return(node):
    """Convert a return node to valid c return statement."""
    return cgen.Statement("return {}".format(convert_expression(node.value)))


def convert_function_def(node, frame):
    """Convert a python function definition to a valid c function definition.
    This function also adds the current function to the frame.
    """
    name = node.name
    args = node.args
    body = node.body
    decs = node.decorator_list
    returns = node.returns

    # Add the current function to the frame
    func_ret_type = determine_variable_type(returns)
    frame[name] = func_ret_type

    return cgen.FunctionBody(
        cgen.FunctionDeclaration(
            convert_variable_declaration(returns, name),
            convert_argument_declarations(args)
        ),
        cgen.Block(contents=convert_body(body, frame))
    )


def convert_assign(node, frame):
    """Convert a variable assignment to valid c declaration.

    TODO: Add checking for if using global statement to use global variable."""
    lhs = node.targets
    rhs = node.value

    # Accept only single assignments for now
    # TODO: Implement unpacking of multiple variables
    # TODO: Implement assignment of multiple variables
    lhs = lhs[0]
    name = lhs.id

    rvalue = convert_expression(rhs)
    if name not in frame:
        # The rhs is either a function or a hardcoded value.
        # Extract this type.
        var_type = determine_expr_type(rhs, frame)
        lvalue = cgen.Value(var_type, name).inline(with_semicolon=False)
    else:
        lvalue = name

    return cgen.Assign(
        lvalue=lvalue,
        rvalue=rvalue
    )


def convert_statement(node, frame):
    """Ceck for the type of statement and convert it appropriately.
    If the frame can be changed such as in an assignment, the frame
    may also be changed."""
    if isinstance(node, ast.Module):
        return convert_module(node)
    elif isinstance(node, ast.FunctionDef):
        return convert_function_def(node, frame)
    elif isinstance(node, ast.Return):
        return convert_return(node)
    elif isinstance(node, ast.Expr):
        return cgen.Statement(convert_expression(node.value))
    elif isinstance(node, ast.Assign):
        return convert_assign(node, frame)
    else:
        raise RuntimeError("Unknown statement \n{}".format(prettyparsetext(node)))


def convert_body(nodes, frame):
    """Convert individual statements in a body of code to valid c code.
    The frame is copied for new function bodies.

    TODO: Allow for variables declared in bodies of if statements and
    while/for loops to persist out of that body."""
    local_frame = {k: v for k, v in frame.items()}
    return [convert_statement(n, local_frame) for n in nodes if not isinstance(n, ast.Pass)]


def convert_module(node):
    """Convert a python module to a block of c code."""
    return cgen.Module(
        contents=convert_body(node.body, {})
    )


