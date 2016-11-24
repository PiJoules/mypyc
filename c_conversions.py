# -*- coding: utf-8 -*-

"""
Functions for converting nodes of the python ast to nodes of the c ast.
"""

from utils import *
from features import *

import cgen
import ast


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


BUILTIN_MODULES = set([
    "math",
])


def convert_variable_declaration(node, name):
    """Convert a python variable declaration to a c declaration."""
    return cgen.Value(determine_variable_type(node), name)


def convert_argument_declarations(args):
    """Convert a list of argument declarations to c argument declarations."""
    return [convert_variable_declaration(a.annotation, a.arg) for a in args.args]


def convert_operation(node):
    """Convert a binary or unary operand to the corresponding valid c operation."""
    # TODO: Check python version for @ operation, matrix multiplication (v3.5)
    if isinstance(node, (ast.Add, ast.UAdd)):
        return "+"
    elif isinstance(node, (ast.Sub, ast.USub)):
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
    elif isinstance(node, ast.Not):
        return "!"
    elif isinstance(node, ast.Invert):
        return "~"
    elif isinstance(node, ast.And):
        return "&&"
    elif isinstance(node, ast.Or):
        return "||"
    elif isinstance(node, (ast.Eq, ast.Is)):
        # TODO: Implement separate logic for is
        return "=="
    elif isinstance(node, (ast.NotEq, ast.IsNot)):
        # TODO: Implement separate logic for is not
        return "!="
    elif isinstance(node, ast.Lt):
        return "<"
    elif isinstance(node, ast.LtE):
        return "<="
    elif isinstance(node, ast.Gt):
        return ">"
    elif isinstance(node, ast.GtE):
        return ">="
    elif isinstance(node, (ast.In, ast.NotIn)):
        raise RuntimeError("TODO: Implement logic for in and not in operations")
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
        return convert_attribute(node)
    elif isinstance(node, ast.UnaryOp):
        return convert_unary_operation(node, frame)
    elif isinstance(node, (ast.BoolOp, ast.Compare)):
        return convert_boolean_operation(node, frame)
    else:
        raise RuntimeError("Unknown expression \n{}".format(node))


def convert_unary_operation(node, frame):
    """Convert a unary operation to valid c representation."""
    return "{}({})".format(
        convert_operation(node.op),
        convert_expression(node.operand, frame)
    )


def convert_binary_operation(node, frame):
    """Convert a binary operation to the corresponding valid c code."""
    return "({}) {} ({})".format(
        convert_expression(node.left, frame),
        convert_operation(node.op),
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


def convert_attribute(node):
    """Convert accessing an attribute in a python object to the valid c representation."""
    if isinstance(node, ast.Attribute):
        return convert_attribute(node.value) + "->" + node.attr
    elif isinstance(node, ast.Name):
        if node.id in BUILTIN_MODULES:
            return "p_" + node.id + "_module"
        return node.id
    else:
        raise RuntimeError("Unknown attribute type {}".format(node))


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
    name = convert_attribute(node.func)

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

    # Create local frame internal to function
    local_frame = {k: v for k, v in frame.items()}
    for arg in args.args:
        local_frame[arg.arg] = determine_variable_type(arg.annotation)

    return cgen.FunctionBody(
        cgen.FunctionDeclaration(
            convert_variable_declaration(returns, name),
            convert_argument_declarations(args)
        ),
        cgen.Block(contents=convert_body(body, local_frame))
    )


def convert_assignment(node, frame, assign_op="="):
    """Convert a variable assignment to valid c declaration.

    TODO: Add checking for if using global statement to use global variable.

    Returns:
        cgen.Assign
    """
    lhs = node.targets
    rhs = node.value

    # Accept only single assignments for now
    # TODO: Implement unpacking of multiple variables
    # TODO: Implement assignment of multiple variables
    lhs = lhs[0]
    name = lhs.id

    rvalue = convert_expression(rhs, frame)
    return convert_assignment_from_parts(name, rhs, frame, assign_op=assign_op)


def convert_assignment_from_parts(target_name, rhs_node, frame, assign_op="="):
    if target_name not in frame:
        target_type = determine_expr_type(rhs_node, frame)
        frame[target_name] = target_type
        lvalue = convert_value_declaration(target_type, target_name)
    else:
        lvalue = target_name

    return cgen.Statement("{} {} {}".format(lvalue, assign_op, convert_expression(rhs_node, frame)))



def raw_assignment_from_parts(var_type, var_name, rhs):
    """Convert a type, name, and rhs expression to an assignment node.

    Args:
        var_type (str)
        var_name (str)
        rhs (str)

    Returns:
        cgen.Assign
    """
    return cgen.Assign(
        lvalue=convert_value_declaration(var_type, var_name),
        rvalue=rhs
    )


def convert_import(node):
    """Convert a single python import to a list of c includes."""
    imports = []
    for alias in node.names:
        IMPORTED_MODULES.add(alias.name)
        imports.append(cgen.Include("p_" + alias.name + ".h"))
    return imports


def convert_range_to_params(node, frame):
    """Find the starting value, ending value, and step for a range function call.

    Args:
        node: (ast.Call): the range function call

    Returns:
        str: start
        str: end
        str: step
    """
    args = node.args
    if len(args) == 1:
        return "0", convert_expression(node.args[0], frame), "1"
    elif len(args) == 2:
        return (
            convert_expression(node.args[0], frame),
            convert_expression(node.args[1], frame),
            "1"
        )
    else:
        return (
            convert_expression(node.args[0], frame),
            convert_expression(node.args[1], frame),
            convert_expression(node.args[2], frame)
        )


def convert_value_declaration(var_type, var_name, with_semicolon=False):
    """Wrapper for cgen.Value."""
    return cgen.Value(var_type, var_name).inline(with_semicolon=with_semicolon)


def regular_iteration(node, frame):
    """Regular for loop iteration in c from python for loop iteration using
    range.

    Returns:
        cgen.For
    """
    iter_val = node.target
    iterable = node.iter
    body = node.body
    orelse = node.orelse

    start, stop, step = convert_range_to_params(iterable, frame)

    local_frame = {k: v for k, v in frame.items()}
    local_frame[iter_val.id] = "int"

    return cgen.For(
        str(raw_assignment_from_parts("int", iter_val.id, start))[:-1],  # last part has extra semicolon
        "{} < {}".format(iter_val.id, stop),
        "{} += {}".format(iter_val.id, step),
        cgen.Block(contents=convert_body(body, local_frame))
    )


def convert_for_loop(node, frame):
    """Convert a python for loop to a c for loop.
    If using range, convert to for loop iteration in c.
    """
    iter_val = node.target
    iterable = node.iter
    body = node.body
    orelse = node.orelse

    # TODO: Implement orelse logic
    # Move into orelse block if we do not break out this for loop

    if isinstance(iterable, ast.Call) and iterable.func.id == "range":
        # Iteration
        return regular_iteration(node, frame)

    raise RuntimeError("TODO: Implement iterator logic")


def convert_comparison(node, frame):
    """Convert a multi-comparison boolean operation to a conjunction of the
    individual comparisons.

    Returns:
        str
    """
    if len(node.ops) == 1:
        return "{} {} {}".format(
            convert_expression(node.left, frame),
            convert_operation(node.ops[0]),
            convert_expression(node.comparators[0], frame)
        )

    # Create list of size 1 comparisons
    values = [Compare(
        left=node.left,
        ops=[node.ops[0]],
        comparators=[node.comparators[0]]
    )]
    for i in range(1, len(node.ops)):
        values.append(Compare(
            left=node.comparators[i-1],
            ops=[node.ops[i]],
            comparators=[node.comparators[i]]
        ))

    return convert_boolean_operation(
        ast.BoolOp(
            op=ast.And(),
            values=values
        ),
        frame
    )


def convert_boolean_operation(node, frame):
    """Convert a boolean operation/comparison to c representation.

    Returns:
        str
    """
    if isinstance(node, ast.Compare):
        return convert_comparison(node, frame)

    if isinstance(node, ast.UnaryOp):
        return convert_unary_operation(node, frame)

    delimiter = " {} ".format(convert_operation(node.op))
    return delimiter.join("({})".format(convert_expression(n, frame)) for n in node.values)


def convert_if(node, frame):
    """Convert python if statement to c if statement.
    If/elif/else ladders are nested if else nodes"""
    condition = node.test
    body = node.body
    orelse = node.orelse  # list

    if orelse:
        if len(orelse) == 1 and isinstance(orelse[0], ast.If):
            # elif ladder
            rest = convert_if(orelse[0], frame)
        else:
            rest = cgen.Block(contents=convert_body(orelse, frame))
    else:
        rest = None

    return cgen.If(
        convert_boolean_operation(condition, frame), # str
        cgen.Block(contents=convert_body(body, frame)), # block
        else_=rest
    )


def convert_while(node, frame):
    """Convert a while statement to valid c version."""
    condition = node.test
    body = node.body
    orelse = node.orelse

    # TODO: Add logic for orelse statememts

    return cgen.While(
        convert_boolean_operation(condition, frame),
        cgen.Block(contents=convert_body(body, frame))
    )


def convert_augmented_assignment(node, frame):
    """Convert aug assignments (+=, -=, *=) to valid c representations."""
    return convert_assignment_from_parts(
        node.target.id, node.value, frame,
        assign_op=convert_operation(node.op) + "=")


def convert_statement(node, frame):
    """Ceck for the type of statement and convert it appropriately.
    If the frame can be changed such as in an assignment, the frame
    may also be changed.

    Returns:
        cgen.Generable: the corresponding c ast node
    """
    if isinstance(node, ast.FunctionDef):
        return convert_function_def(node, frame)
    elif isinstance(node, ast.Return):
        return convert_return(node, frame)
    elif isinstance(node, ast.Expr):
        return cgen.Statement(convert_expression(node.value, frame))
    elif isinstance(node, ast.Assign):
        return convert_assignment(node, frame)
    elif isinstance(node, ast.Import):
        raise RuntimeError("Imports should have already been processed beforehand.")
    elif isinstance(node, ast.For):
        return convert_for_loop(node, frame)
    elif isinstance(node, ast.If):
        return convert_if(node, frame)
    elif isinstance(node, ast.While):
        return convert_while(node, frame)
    elif isinstance(node, ast.AugAssign):
        return convert_augmented_assignment(node, frame)
    else:
        raise RuntimeError("Unknown statement \n{}".format(node))


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


