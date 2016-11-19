from __future__ import print_function

import cgen
import ast


from translate import prettyparseprint


class Function(object):
    def __init__(self, name):
        self.__name = name
        self.__return_types = []
        self.__args = []

    def add_args(self, arg):
        self.__args.append(arg)

    def return_types(self):
        return self.__return_types

    def name(self):
        return self.__name


class Variable(object):
    def __init__(self, name):
        self.__types = []
        self.__name = name

    def add_type(self, t):
        self.__types.append(t)

    def name(self):
        return self.__name

    def types(self):
        return self.__types


def parse_module_node(node):
    return cgen.Module(contents=parse_node_body(node.body))


def parse_value(node):
    """Return back the value and type representation."""
    if isinstance(node, ast.Num):
        return node.n
    else:
        raise RuntimeError("Unknown value type {}".format(node))


def main_function_declaration():
    return cgen.FunctionDeclaration(
        cgen.Value("int", "main"),
        [
            cgen.Value("int", "argc"),
            cgen.Value("char*", "argv[]")
        ]
    )


def parse_function_declaration(name, args):
    if name == "main":
        return main_function_declaration()
    else:
        raise RuntimeError("TODO: Implement search to determine types")


def evaluate_func_ret_type(node_body):
    pass


def parse_function_def(node):
    # Need to evaluate return type and arg types

    name = node.name
    args = node.args
    body = node.body
    decs = node.decorator_list

    ret_type = evaluate_func_ret_type(body)

    return cgen.FunctionBody(
        parse_function_declaration(name, args),
        cgen.Block(contents=parse_node_body(body)),
    )


def parse_return(node):
    return cgen.Statement("return {}".format(parse_value(node.value)))


def parse_node_body(body):
    body_block = []
    for node in body:
        if isinstance(node, ast.Module):
            body_block.append(parse_module(node))
        elif isinstance(node, ast.FunctionDef):
            body_block.append(parse_function_def(node))
        elif isinstance(node, ast.Return):
            body_block.append(parse_return(node))
        else:
            raise RuntimeError("Unknown node type {}".format(node))
    return body_block


def c_ast_from_python_ast(p_ast):
    return parse_module_node(p_ast)


def file_to_python_ast(filename):
    with open(filename, "r") as f:
        return code_to_python_ast(f.read())


def code_to_python_ast(code):
    return ast.parse(code)


def main():
    p_ast = file_to_python_ast("test_py_files/1.py")
    prettyparseprint(p_ast)

    c_ast = c_ast_from_python_ast(p_ast)
    print(c_ast)

    return 0


if __name__ == "__main__":
    main()

