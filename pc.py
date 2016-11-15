from __future__ import print_function

import cgen
import ast


from translate import prettyparseprint


def parse_module_node(node):
    return cgen.Module(contents=parse_node_body(node.body))


def parse_value(node):
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


def parse_function_def(node):
    name = node.name
    args = node.args
    body = node.body
    decs = node.decorator_list
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


def code_to_python_ast(code):
    return ast.parse(code)


def main():
    p_str = """
def main(argc, argv):
    return 0
    """

    p_ast = code_to_python_ast(p_str)
    prettyparseprint(p_ast)

    c_ast = c_ast_from_python_ast(p_ast)
    print(c_ast)

    return 0


if __name__ == "__main__":
    main()

