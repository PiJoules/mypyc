#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cast
import ast_utils
import ast
import inference as inf


def convert_type(infer_type):
    """
    Convert an inference type to a cast type.
    """
    if isinstance(infer_type, inf.NoneType):
        return cast.VoidType()
    elif isinstance(infer_type, inf.IntType):
        return cast.IntType()

    raise NotImplementedError("Unable to convert type {}".format(infer_type))


class Compiler(object):
    @classmethod
    def from_code(cls, code, **kwargs):
        return cls(ast.parse(code), **kwargs)

    def __init__(self, py_ast):
        self.__ast = py_ast

        # Find all types
        self.__env = inf.Environment(init_node=py_ast)
        self.__c_ast = self.parse(self.__ast)

    def parse_sequence(self, seq):
        """
        Returns:
            list[cast.Node]
        """
        return [self.parse(node) for node in seq]

    def parse_module(self, node):
        """
        Returns:
            cast.Module
        """
        return cast.Module(self.parse_sequence(node.body))

    def parse_func_def(self, node):
        """
        Just parse positional args for now.

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

        # Positional args
        arg_decls = []
        for arg in pos_args:
            types = env.lookup(name)

            # Handle only vars of one type for now
            if len(types) != 1:
                raise NotImplementedError("No handling of variables with multiple types yet.")

            t = next(iter(types))
            cast_type = convert_type(t)
            decl = cast.VariableDeclaration(cast_type, arg.arg)
            arg_decls.append(decl)

        # Body

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
        return cast.Return(self.parse(node.value))

    def parse_num(self, node):
        n = node.n
        if isinstance(n, int):
            return cast.IntLiteral(n)
        elif isinstance(n, float):
            return cast.FloatLiteral(n)
        elif isinstance(n, complex):
            raise NotImplementedError("No default type for complex numbers yet.")

        raise RuntimeError("Unknown num literal type for number of type {}".format(type(n)))

    def parse(self, node):
        """
        Returns:
            cast.Node
        """
        if isinstance(node, ast.Module):
            return self.parse_module(node)
        elif isinstance(node, ast.FunctionDef):
            return self.parse_func_def(node)
        elif isinstance(node, ast.Return):
            return self.parse_return(node)
        elif isinstance(node, ast.Num):
            return self.parse_num(node)

        raise NotImplementedError("Unable to parse node {}".format(node))

    def ast(self):
        return self.__c_ast


def compile_code(code):
    compiler = Compiler.from_code(code)
    return compiler.ast()


def compile_file(filename):
    with open(filename, "r") as f:
        return compile_code(f.read())


def main():
    code = """
def main():
    return 0
    """

    compiler = Compiler.from_code(code)
    print(compiler.ast())

    return 0


if __name__ == "__main__":
    main()

