#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import cgen
import os
import subprocess

from translate import *


def ast_from_file(filename):
    with open(filename, "r") as f:
        return generate_ast(f.read())


def generate_ast(code):
    node = ast.parse(code)
    return node


def parse_var_decl(node, name):
    if node is None:
        return cgen.Value("void", name)
    elif isinstance(node, ast.Name):
        if node.id == "str":
            return cgen.Pointer(cgen.Value("char", name))
        else:
            return cgen.Value(node.id, name)
    elif isinstance(node, ast.List):
        return cgen.Pointer(parse_var_decl(node.elts[0], name))
    else:
        raise RuntimeError("Unknown return type declaration '{}'".format(node))


def parse_arg_decl(arg):
    return parse_var_decl(
        arg.annotation,
        arg.arg
    )


def parse_arg_decls(args):
    pos_args = [parse_arg_decl(a) for a in args.args]
    return pos_args


def parse_function_declaration(name, args, returns):
    return cgen.FunctionDeclaration(
        parse_var_decl(returns, name),
        parse_arg_decls(args)
    )


def parse_op(node):
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


def parse_bin_op(node):
    return "{} {} {}".format(
        parse_expr(node.left),
        parse_op(node.op),
        parse_expr(node.right)
    )


def parse_call(node):
    return "{name}({args})".format(
        name=parse_expr(node.func),
        args=", ".join([parse_expr(a) for a in node.args])
    )


def parse_expr(node):
    if isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Str):
        return "\"{}\"".format(node.s)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.BinOp):
        return parse_bin_op(node)
    elif isinstance(node, ast.Call):
        return parse_call(node)
    else:
        raise RuntimeError("Unknown expression \n{}".format(prettyparsetext(node)))


def parse_return(node):
    return cgen.Statement("return {}".format(parse_expr(node.value)))


def function_frame(args):
    prettyparseprint(args)


def parse_function_def(node):
    name = node.name
    args = node.args
    body = node.body
    decs = node.decorator_list
    returns = node.returns

    init_frame = function_frame(args)
    contents = parse_body(body)
    block = cgen.Block(contents=contents)

    return cgen.FunctionBody(
        parse_function_declaration(name, args, returns),
        block
    )


def parse_statement(node):
    if isinstance(node, ast.Module):
        return parse_module(node)
    elif isinstance(node, ast.FunctionDef):
        return parse_function_def(node)
    elif isinstance(node, ast.Return):
        return parse_return(node)
    elif isinstance(node, ast.Expr):
        return cgen.Statement(parse_expr(node.value))
    elif isinstance(node, ast.Assign):
        raise RuntimeError("TODO: Implement Assignment")
    else:
        raise RuntimeError("Unknown statement \n{}".format(prettyparsetext(node)))


def parse_body(nodes, frame=None):
    if frame is None:
        frame = {}
    return [parse_statement(n) for n in nodes if not isinstance(n, ast.Pass)]


def parse_module(node):
    return cgen.Module(
        contents=parse_body(node.body)
    )


def main() -> int:
    filename = "test.py"
    node = ast_from_file(filename)

    prettyparseprint(node)
    c_code = str(parse_module(node))
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
