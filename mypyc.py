#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import cgen
import os
import subprocess

from translate import *


GLOBAL_FRAME = {}


def ast_from_file(filename):
    with open(filename, "r") as f:
        return generate_ast(f.read())


def generate_ast(code):
    node = ast.parse(code)
    return node


def convert_var_decl(node, name):
    return cgen.Value(evaluate_var_type(node), name)


def evaluate_var_type(node):
    if node is None:
        return "void"
    elif isinstance(node, ast.Name):
        if node.id == "str":
            return "char*"
        else:
            return node.id
    elif isinstance(node, ast.List):
        return evaluate_var_type(node.elts[0]) + "*"
    else:
        raise RuntimeError("Unknown var type '{}'".format(node))


def convert_arg_decl(arg):
    return convert_var_decl(
        arg.annotation,
        arg.arg
    )


def convert_arg_decls(args):
    pos_args = [convert_arg_decl(a) for a in args.args]
    return pos_args


def convert_function_declaration(name, args, returns, frame):
    func_ret_type = evaluate_var_type(returns)
    frame[name] = func_ret_type

    return cgen.FunctionDeclaration(
        convert_var_decl(returns, name),
        convert_arg_decls(args)
    )


def convert_op(node):
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


def convert_bin_op(node):
    return "{} {} {}".format(
        convert_expr(node.left),
        convert_op(node.op),
        convert_expr(node.right)
    )


def convert_call(node):
    return "{name}({args})".format(
        name=convert_expr(node.func),
        args=", ".join([convert_expr(a) for a in node.args])
    )


def convert_expr(node):
    if isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Str):
        return "\"{}\"".format(node.s)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.BinOp):
        return convert_bin_op(node)
    elif isinstance(node, ast.Call):
        return convert_call(node)
    else:
        raise RuntimeError("Unknown expression \n{}".format(prettyparsetext(node)))


def convert_return(node):
    return cgen.Statement("return {}".format(convert_expr(node.value)))


def convert_function_def(node, frame):
    name = node.name
    args = node.args
    body = node.body
    decs = node.decorator_list
    returns = node.returns

    contents = convert_body(body, frame)
    block = cgen.Block(contents=contents)

    return cgen.FunctionBody(
        convert_function_declaration(name, args, returns, frame),
        block
    )


def evaluate_literal_type(expr):
    if isinstance(expr, ast.Num):
        return "int"
    elif isinstance(expr, ast.Str):
        return "char*"
    else:
        raise RuntimeError("Unknown literal type\n{}".format(prettyparsetext(expr)))


def evaluate_function_return_type(func, frame):
    name = func.func.id
    if name not in frame:
        raise RuntimeError("Function '{}' was not declared beforehand.".format(name))
    return frame[name]


def evaluate_expr_type(expr, frame):
    if isinstance(expr, ast.Call):
        return evaluate_function_return_type(expr, frame)
    elif isinstance(expr, ast.Name):
        return frame[expr.id]
    else:
        return evaluate_literal_type(expr)


def convert_assign(node, frame):
    lhs = node.targets
    rhs = node.value

    lhs = lhs[0]
    name = lhs.id

    rvalue = convert_expr(rhs)
    if name not in frame:
        # The rhs is either a function or a hardcoded value.
        # Extract this type.
        var_type = evaluate_expr_type(rhs, frame)
        lvalue = cgen.Value(var_type, name).inline(with_semicolon=False)
    else:
        lvalue = name

    return cgen.Assign(
        lvalue=lvalue,
        rvalue=rvalue
    )


def convert_statement(node, frame):
    if isinstance(node, ast.Module):
        return convert_module(node)
    elif isinstance(node, ast.FunctionDef):
        return convert_function_def(node, frame)
    elif isinstance(node, ast.Return):
        return convert_return(node)
    elif isinstance(node, ast.Expr):
        return cgen.Statement(convert_expr(node.value))
    elif isinstance(node, ast.Assign):
        return convert_assign(node, frame)
    else:
        raise RuntimeError("Unknown statement \n{}".format(prettyparsetext(node)))


def convert_body(nodes, frame):
    local_frame = {k: v for k, v in frame.items()}
    return [convert_statement(n, local_frame) for n in nodes if not isinstance(n, ast.Pass)]


def convert_module(node):
    return cgen.Module(
        contents=convert_body(node.body, GLOBAL_FRAME)
    )


def main():
    filename = "test.py"
    node = ast_from_file(filename)

    prettyparseprint(node)
    c_code = str(convert_module(node))
    print(c_code)


    # Save into c file and compile
    base_name, ext = os.path.splitext(filename)
    c_file = base_name + ".c"
    with open(c_file, "w") as f:
        f.write(c_code)

    cmd = "{compiler} -std={standard} -o {output} {files}"
    cmd = cmd.format(
        compiler="gcc",
        standard="c11",
        output=base_name,
        files=" ".join([c_file])
    )
    assert not subprocess.check_call(cmd.split())


    return 0


if __name__ == "__main__":
    main()
