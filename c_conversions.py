# -*- coding: utf-8 -*-

"""
Functions for converting nodes of the python ast to nodes of the c ast.
"""

from utils import *

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
        if expr.id not in frame:
            raise RuntimeError("Unable to find variable/function '{}' in frame: {}".format(expr.id, list(frame.keys())))
        return frame[expr.id]
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


"""
Conversions
"""


# Nodes that are allowed to stay in the body of a module without having to be
# wrapped in a function
VALID_MODULE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.Assign,
)


IMPORTED_MODULES = set()


BUILTIN_FUNCTIONS = set([
    "print",
])


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


def convert_expression(node, frame):
    """Convert a python expression to the valid c code.

    Returns:
        str: The string representation of the c expression.
    """
    if isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Str):
        return "\"{}\"".format(node.s)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.BinOp):
        return convert_binary_operation(node, frame)
    elif isinstance(node, ast.Call):
        return convert_call(node, frame)
    elif isinstance(node, ast.Attribute):
        return convert_attribute(node, frame)
    else:
        raise RuntimeError("Unknown expression \n{}".format(prettyparsetext(node)))


def convert_binary_operation(node, frame):
    """Convert a binary operation to the corresponding valid c code."""
    return "{} {} {}".format(
        convert_expression(node.left, frame),
        convert_operand(node.op),
        convert_expression(node.right, frame)
    )


def convert_print_format(expr, frame):
    """Convert an expression to the appropriate format specifier and valid
    c representation.

    Returns:
        str: Format specifier
        str: c expression
    """
    expr_type = determine_expr_type(expr, frame)
    expr_fmt = convert_expression(expr, frame)
    return expr_type, expr_fmt


def convert_multiple_arg_print(node, frame):
    """Convert a multiple argument print statement.
    Join all arguments by a single space.

    print(expr1, expr2, expr3, ...)
    """
    args = node.args
    fmt_specifiers = []
    exprs = []

    for arg in args:
        fmt_specifiers.append(determine_format_specifier(arg, frame))
        exprs.append(convert_expression(arg, frame))

    return "printf(\"{fmt_specifiers}\\n\", {exprs})".format(
        fmt_specifiers=" ".join(fmt_specifiers),
        exprs=", ".join(exprs)
    )


def convert_print(node, frame):
    """Convert specific print statements to print formats."""
    if len(node.args) == 1:
        arg = node.args[0]
        arg_type = determine_expr_type(arg, frame)
        if arg_type == "int":
            # TODO: Ensure that propper includes are added at the start of the
            # file
            return "printf(\"%d\\n\", {})".format(convert_expression(arg, frame))
        elif arg_type == "char*":
            return "printf(\"%s\\n\", {})".format(convert_expression(arg, frame))
        elif arg_type == "float":
            return "printf(\"%f\\n\", {})".format(convert_expression(arg, frame))
        else:
            raise RuntimeError("TODO: Implement handling of single print argument of type '{}'".format(arg_type))
    else:
        return convert_multiple_arg_print(node, frame)


def convert_attribute(node, frame):
    """Convert accessing an attribute in a python object to the valid c representation."""
    obj_name = node.value.id
    if obj_name in IMPORTED_MODULES:
        # Calling something in another module
        return node.attr
    else:
        raise RuntimeError("TODO: Handle accessing attributes from something other than an imported module.")


def convert_builtin_function(node, frame):
    if node.func.id == "print":
        return convert_print(node, frame)
    else:
        raise RuntimeError("Unknown builtin function {}".format(node.func.id))


def convert_call(node, frame):
    """Convert a python function call to the valid c representation.

    Returns:
        str: The string representation of the equivalent c call.
    """
    if isinstance(node.func, ast.Attribute):
        name = node.func.attr
    else:
        name = node.func.id

    if name in BUILTIN_FUNCTIONS:
        return convert_builtin_function(node, frame)

    return "{name}({args})".format(
        name=name,
        args=", ".join(convert_expression(a, frame) for a in node.args)
    )


def convert_return(node, frame):
    """Convert a return node to valid c return statement."""
    return cgen.Statement("return {}".format(convert_expression(node.value, frame)))


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

    rvalue = convert_expression(rhs, frame)
    if name not in frame:
        # The rhs is either a function or a hardcoded value.
        # Extract this type.
        var_type = determine_expr_type(rhs, frame)
        frame[name] = var_type
        lvalue = cgen.Value(var_type, name).inline(with_semicolon=False)
    else:
        lvalue = name

    return cgen.Assign(
        lvalue=lvalue,
        rvalue=rvalue
    )


def convert_import(node):
    """Convert a single python import to a list of c includes."""
    imports = []
    for alias in node.names:
        IMPORTED_MODULES.add(alias.name)
        imports.append(cgen.Include("p_" + alias.name + ".h"))
    return imports


def convert_statement(node, frame):
    """Ceck for the type of statement and convert it appropriately.
    If the frame can be changed such as in an assignment, the frame
    may also be changed."""
    if isinstance(node, ast.FunctionDef):
        return convert_function_def(node, frame)
    elif isinstance(node, ast.Return):
        return convert_return(node, frame)
    elif isinstance(node, ast.Expr):
        return cgen.Statement(convert_expression(node.value, frame))
    elif isinstance(node, ast.Assign):
        return convert_assign(node, frame)
    elif isinstance(node, ast.Import):
        raise RuntimeError("Imports should have already been processed beforehand.")
    else:
        raise RuntimeError("Unknown statement \n{}".format(prettyparsetext(node)))


def convert_body(nodes, frame):
    """Convert individual statements in a body of code to valid c code.
    The frame is copied for new function bodies.

    TODO: Allow for variables declared in bodies of if statements and
    while/for loops to persist out of that body."""
    local_frame = {k: v for k, v in frame.items()}
    body = []

    # Handle all imports first
    for node in nodes:
        if isinstance(node, ast.Import):
            body += convert_import(node)

    # Convert remaining nodes that aren't pass or import
    body += [convert_statement(n, local_frame) for n in nodes if not isinstance(n, (ast.Pass, ast.Import))]

    return body


def convert_module(node):
    """Convert a python module to a block of c code."""

    body = [cgen.Include("mypyc.h")]
    body += convert_body([n for n in node.body if isinstance(n, VALID_MODULE_NODES)], {})

    return cgen.Module(contents=body)


