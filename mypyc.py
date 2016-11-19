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
    if isinstance(node, ast.Name):
        if node.id == "str":
            return cgen.Pointer(cgen.Value("char", name))
        else:
            return cgen.Value(node.id, name)
    elif isinstance(node, ast.List):
        return cgen.Pointer(parse_var_decl(node.elts[0], name))
    else:
        raise RuntimeError("Unknown return type declaration {}".format(node))


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


def parse_expr(node):
    if isinstance(node, ast.Num):
        return node.n
    else:
        raise RuntimeError("Unknown expression {}".format(node))


def parse_return(node):
    return cgen.Statement("return {}".format(parse_expr(node.value)))


def parse_function_def(node):
    name = node.name
    args = node.args
    body = node.body
    decs = node.decorator_list
    returns = node.returns

    return cgen.FunctionBody(
        parse_function_declaration(name, args, returns),
        cgen.Block(
            contents=parse_body(body)
        )
    )


def parse_statement(node):
    if isinstance(node, ast.Module):
        return parse_module(node)
    elif isinstance(node, ast.FunctionDef):
        return parse_function_def(node)
    elif isinstance(node, ast.Return):
        return parse_return(node)
    else:
        raise RuntimeError("Unknown node type {}".format(node))


def parse_body(nodes):
    return [parse_statement(n) for n in nodes]


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
