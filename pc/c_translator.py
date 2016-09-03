#-*- coding: utf-8 -*-

from rules import *


NEWLINE = "\n"
LINE_END = ";"
LINE_DELIM = LINE_END + NEWLINE
ARG_SEPARATOR = ", "


class CTranslator(object):
    """Translates a parse tree to C code."""

    def __init__(self, parse_tree, indentation_size=4):
        self.__parse_tree = parse_tree
        self.__indent_size = indentation_size

    def join_body(self, body):
        """Just join a list of strings and add the line ending to result."""
        return LINE_DELIM.join(body) + LINE_END

    def translate_function_argument(self, arg):
        code_str = "{type} {name}"
        return code_str.format(
            type=arg.type,
            name=arg.name,
        )

    def translate_function_def(self, func_def, indentation_level):
        code_str = "{return_type} {func_name}({func_args}){{\n{func_body}\n}}"

        return_type = func_def.return_type
        func_name = func_def.name
        func_args = [self.translate_function_argument(arg) for arg in func_def.args]
        func_body = [self.translate_statement(s, indentation_level+1) for s in func_def.body]

        return code_str.format(
            return_type=return_type,
            func_name=func_name,
            func_args=ARG_SEPARATOR.join(func_args),
            func_body=self.join_body(func_body),
        )

    def translate_function_call(self, call):
        code_str = "{func_name}({func_args})"

        func_name = call.name
        func_args = [self.translate_expression(a) for a in call.args]

        return code_str.format(
            func_name=func_name,
            func_args=ARG_SEPARATOR.join(func_args),
        )

    def translate_return_statement(self, return_statement):
        code_str = "return {ret_value}"
        return code_str.format(
            ret_value=self.translate_expression(return_statement.return_value),
        )

    def translate_macro(self, macro):
        return macro.line

    def translate_literal(self, literal):
        if isinstance(literal, StringLiteral):
            return literal.value
        elif isinstance(literal, NumberLiteral):
            return str(literal.value)

        raise RuntimeError("Unknown literal '{}'".format(literal))

    def translate_expression(self, expression):
        if isinstance(expression, Literal):
            return self.translate_literal(expression)

        raise RuntimeError("Unknown expression '{}'".format(expression))

    def translate_statement(self, statement, indentation_level):
        """Hanlde different types of statements in the body of something."""
        padding = " " * indentation_level * self.__indent_size
        if isinstance(statement, FunctionDefinition):
            statement = self.translate_function_def(statement, indentation_level)
        elif isinstance(statement, FunctionCall):
            statement = self.translate_function_call(statement)
        elif isinstance(statement, ReturnStatement):
            statement = self.translate_return_statement(statement)
        elif isinstance(statement, Macro):
            statement = self.translate_macro(statement)
        else:
            raise RuntimeError("Unable to handle statement '{}'".format(statement))

        return padding + statement

    def translate_module(self, module):
        lines = [self.translate_statement(s, 0) for s in module.body]
        return NEWLINE.join(lines)

    def translate(self):
        """Return the whole resulting string of code."""
        return self.translate_module(self.__parse_tree)

