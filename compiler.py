#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cast
import ast_utils
import ast
import inference as inf
import os
import subprocess
import json


def convert_type(infer_type):
    """
    Convert an inference type to a cast type.
    """
    if isinstance(infer_type, inf.NoneType):
        return cast.VoidType()
    elif isinstance(infer_type, inf.IntType):
        return cast.IntType()

    raise NotImplementedError("Unable to convert type {}".format(infer_type))


def convert_operator(op):
    """
    Convert an ast operand node to a cast operand node.
    """
    if isinstance(op, ast.And):
        return cast.And()
    elif isinstance(op, ast.Or):
        return cast.Or()
    elif isinstance(op, ast.Lt):
        return cast.Lt()
    elif isinstance(op, ast.Add):
        return cast.Add()
    elif isinstance(op, ast.Sub):
        return cast.Sub()

    raise NotImplementedError("TODO: Implement convertion for operator {}".format(op))


"""
Headers required for specific functions and variables used.
"""
REQUIRED_HEADERS = {
    "print": {"iostream"},
}


class Compiler(object):
    @classmethod
    def from_code(cls, code, **kwargs):
        return cls(ast.parse(code), **kwargs)

    def __init__(self, py_ast):
        self.__ast = py_ast
        self.__headers = set()  # set[str]

        # Find all types
        self.__env = inf.Environment(init_node=py_ast)
        self.__c_ast = self.parse_statement(self.__ast)

    def parse_sequence(self, seq):
        """
        Returns:
            list[cast.Node]
        """
        return [self.parse_statement(node) for node in seq]

    def parse_module(self, node):
        """
        Parse the module, then prepend any headers accumulated.

        Returns:
            cast.Module
        """
        body = self.parse_sequence(node.body)
        if self.__headers:
            body = [cast.Include(h) for h in self.__headers] + body
        return cast.Module(body)

    def parse_func_def(self, node):
        """
        Just parse_statement positional args for now.

        Returns:
            cast.FunctionDefinition
        """
        name = node.name

        args = node.args
        if args.vararg:
            raise NotImplementedError("No handling of *args yet.")
        if args.kwarg:
            raise NotImplementedError("No handling of **kwargs yet.")
        if args.defaults:
            raise NotImplementedError("No handling of keyword arguments yet.")

        pos_args = args.args
        env = self.__env
        types = env.lookup(name)

        # Handle only vars of one type for now
        if len(types) != 1:
            raise NotImplementedError("No handling of variables with multiple types yet.")

        # The actual function type
        func = next(iter(types))
        func_env = func.environment()

        # Positional args
        arg_decls = []
        for arg in pos_args:
            func_arg_types = func_env.lookup(arg.arg)

            # Work with only single types for now
            if len(func_arg_types) != 1:
                raise NotImplementedError("No handling of variables with multiple types yet.")
            func_arg_type = next(iter(func_arg_types))

            cast_type = convert_type(func_arg_type)
            decl = cast.VariableDeclaration(cast_type, arg.arg)
            arg_decls.append(decl)

        # Create the function definition
        func = cast.FunctionDefinition(
            return_type=convert_type(
                inf.simple(inf.simple(env.lookup(name)).return_type())
            ),
            name=name,
            args=cast.ArgumentDeclarations(arg_decls),
            body=cast.FunctionBody(self.parse_sequence(node.body))
        )

        return func

    def parse_return(self, node):
        return cast.Return(self.parse_expr(node.value))

    def parse_num(self, node):
        n = node.n
        if isinstance(n, int):
            return cast.IntLiteral(n)
        elif isinstance(n, float):
            return cast.FloatLiteral(n)
        elif isinstance(n, complex):
            raise NotImplementedError("No default type for complex numbers yet.")

        raise RuntimeError("Unknown num literal type for number of type {}".format(type(n)))

    def parse_compare(self, node):
        """
        The binary operation will be a conjunction of the individual
        comparisons.

        Returns:
            cast.BinaryOp
        """
        bin_op = cast.BinaryOp(
            self.parse_expr(node.left),
            convert_operator(node.ops[0]),
            self.parse_expr(node.comparators[0]),
        )
        for i, op in enumerate(node.ops[1:]):
            bin_op = cast.BinaryOp(
                bin_op,
                cast.And(),
                cast.BinaryOp(
                    node.comparators[i-1],
                    convert_operator(op),
                    node.comparators[i],
                )
            )
        return bin_op

    def parse_name(self, node):
        self.__headers |= REQUIRED_HEADERS.get(node.id, set())
        return cast.Variable(node.id)

    def parse_bin_op(self, node):
        return cast.BinaryOp(
            self.parse_expr(node.left),
            convert_operator(node.op),
            self.parse_expr(node.right),
        )

    def create_output_stream(self, node):
        """
        No node for c++ style output streams yet, so use InlineText for now.

        Returns:
            node for c++ style output streams
        """
        if node.starargs:
            raise NotImplementedError("No handling of *args yet.")
        if node.kwargs:
            raise NotImplementedError("No handling of **kwargs yet.")
        if node.keywords:
            raise NotImplementedError("No handling of keyword arguments yet.")

        # Add the iostream header
        self.__headers |= REQUIRED_HEADERS["print"]

        return cast.InlineText(
            "std::cout << {} << std::endl;".format(
                " << ".join(str(self.parse_expr(a)) for a in node.args)
            )
        )

    def parse_call(self, node):
        """
        Just work with positional arguments for now.
        """
        if node.starargs:
            raise NotImplementedError("No handling of *args yet.")
        if node.kwargs:
            raise NotImplementedError("No handling of **kwargs yet.")
        if node.keywords:
            raise NotImplementedError("No handling of keyword arguments yet.")

        return cast.FunctionCall(
            self.parse_expr(node.func),
            [self.parse_expr(a) for a in node.args]
        )

    def parse_expr(self, node):
        """
        Returns:
            cast.Node
        """
        if isinstance(node, ast.Num):
            return self.parse_num(node)
        elif isinstance(node, ast.Expr):
            return self.parse_expr(node.value)
        elif isinstance(node, ast.Str):
            return cast.StringLiteral(node.s)
        elif isinstance(node, ast.Compare):
            return self.parse_compare(node)
        elif isinstance(node, ast.Name):
            return self.parse_name(node)
        elif isinstance(node, ast.BinOp):
            return self.parse_bin_op(node)
        elif isinstance(node, ast.Call):
            return self.parse_call(node)

        raise RuntimeError("Unable to parse expression for node {}".format(node))

    def parse_if(self, node):
        cond = node.test
        body = node.body
        rest = node.orelse

        conds = [cond]
        bodies = [body]
        while rest:
            if len(rest) == 1 and isinstance(rest[0], ast.If):
                # More in the if/elif/else ladder
                conds.append(rest[0].test)
                bodies.append(rest[0].body)
                rest = rest[0]
            else:
                # Add remaining to the body (the else)
                bodies.append(rest)
                break

        if_stmt = cast.If(
            conds=[self.parse_expr(c) for c in conds],
            bodies=[cast.ControlFlowBody(self.parse_sequence(b)) for b in bodies],
        )

        return if_stmt

    def parse_statement(self, node):
        """
        Args:
            node (ast node)

        Returns:
            cast.Node
        """
        if isinstance(node, ast.Module):
            return self.parse_module(node)
        elif isinstance(node, ast.FunctionDef):
            return self.parse_func_def(node)
        elif isinstance(node, ast.Return):
            return self.parse_return(node)
        elif isinstance(node, ast.Expr):
            # Check for special functions
            value = node.value
            if isinstance(value.func, ast.Name) and value.func.id == "print":
                # Will need to eventually check for vars set equal to print()
                return self.create_output_stream(value)
            else:
                return cast.ExprStmt(self.parse_expr(node))
        elif isinstance(node, ast.If):
            return self.parse_if(node)

        raise NotImplementedError("Unable to parse statement {}".format(node))

    def ast(self):
        return self.__c_ast

    def env_json(self):
        return self.__env.json()


def compile_code(code):
    compiler = Compiler.from_code(code)
    return compiler.ast()


def compile_file(filename):
    with open(filename, "r") as f:
        return compile_code(f.read())


def compile_c_file(filename, compiler="g++", standard="c++11", output=None):
    if output is None:
        output, ext = os.path.splitext(filename)

    files = " ".join([filename])

    cmd = "{compiler} -std={standard} -O2 -o {output} {files}".format(**locals())
    assert not subprocess.check_call(cmd.split())


def save_c_code(c_ast, out_filename):
    with open(out_filename, "w") as f:
        f.write(str(c_ast))


def get_args():
    """Argument parser."""
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("filename", help="Python file to compiler.")
    parser.add_argument("-o", "--output",
                        help="Output excutable name.")
    parser.add_argument("-d", "--dump", default=False, action="store_true",
                        help="Dump the evaluated types.")

    return parser.parse_args()


def main():
    args = get_args()

    if args.dump:
        with open(args.filename, "r") as f:
            compiler = Compiler.from_code(f.read())
    elif args.filename:
        c_ast = compile_file(args.filename)
        base_name, ext = os.path.splitext(args.filename)
        c_file = base_name + ".cpp"
        save_c_code(c_ast, c_file)
        compile_c_file(c_file)


    return 0


if __name__ == "__main__":
    main()

