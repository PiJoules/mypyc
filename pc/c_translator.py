#-*- coding: utf-8 -*-

from object_types import *
from actions import *
from literals import *


LINE_END = ";"
LINE_DELIM = LINE_END + "\n"
ARG_SEPARATOR = ", "


class CTranslator(object):
    """Translates a parse tree to C code."""

    def __init__(self, parse_tree, indentation_size=4):
        self.__parse_tree = parse_tree
        self.__indent_size = indentation_size

    def type_to_str(self, t):
        """This language's conversion from the type to a string."""
        if isinstance(t, VoidType):
            return "void"
        elif isinstance(t, IntegerType):
            return "int"
        elif isinstance(t, CharacterType):
            return "char"
        elif isinstance(t, PointerType):
            return self.type_to_str(t.element_type) + "*" * t.depth
        else:
            raise RuntimeError("Unable to hanlde type '{}'".format(t))

    def join_body(self, body):
        """Just join a list of strings and add the line ending to result."""
        return LINE_DELIM.join(body) + LINE_END

    def translate_variable_decl(self, decl):
        code_str = "{type} {name}"
        return code_str.format(
            type=self.type_to_str(decl.type),
            name=decl.name,
        )

    def translate_function_def(self, func_def, indentation_level):
        code_str = "{return_type} {func_name}({func_args}){{\n{func_body}\n}}"

        return_type = self.type_to_str(func_def.return_type)
        func_name = func_def.name
        func_args = [self.translate_variable_decl(decl) for decl in func_def.arg_types]
        func_body = [self.translate_action(a, indentation_level+1) for a in func_def.body]

        return code_str.format(
            return_type=return_type,
            func_name=func_name,
            func_args=ARG_SEPARATOR.join(func_args),
            func_body=self.join_body(func_body),
        )

    def translate_function_call(self, call):
        code_str = "{func_name}({func_args})"

        func_name = call.declaration.name
        func_args = [self.translate_action(a, 0) for a in call.args]

        return code_str.format(
            func_name=func_name,
            func_args=ARG_SEPARATOR.join(func_args),
        )

    def translate_return(self, ret_action):
        code_str = "return {ret_value}"
        return code_str.format(
            ret_value=self.translate_action(ret_action.decl, 0),
        )

    def translate_include(self, include):
        return "#include {lb}{name}{rb}".format(
            lb=include.left_bound,
            name=include.name,
            rb=include.right_bound,
        )

    def translate_action(self, action, indentation_level):
        """Hanlde different types of actions in the body of something."""
        padding = " " * indentation_level * self.__indent_size
        if isinstance(action, FunctionDefinition):
            return padding + self.translate_function_def(action, indentation_level)
        elif isinstance(action, FunctionCall):
            return padding + self.translate_function_call(action)
        elif isinstance(action, Return):
            return padding + self.translate_return(action)
        elif isinstance(action, Literal):
            return str(action)
        elif isinstance(action, Include):
            return self.translate_include(action)
        else:
            raise RuntimeError("Unable to handle action '{}'".format(action))

    def translate_module(self, module):
        lines = [self.translate_action(a, 0) for a in module.body]
        return "\n".join(lines)

    def translate(self):
        """Return the whole resulting string of code."""
        return self.translate_module(self.__parse_tree)

