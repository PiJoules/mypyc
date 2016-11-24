#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import cgen
import os
import subprocess

from utils import *
from c_conversions import *


SOURCE_FILES = [
    "lib/p_math.c",
]


def save_c_code(c_code, filename):
    """Save the covnerted c code from the original python file. If the
    corresponding c file exists, it is overwritten.

    Returns:
        str: Filename the code was saved in."""
    base_name, ext = os.path.splitext(filename)
    c_file = base_name + ".c"
    with open(c_file, "w") as f:
        f.write(c_code)
    return c_file


def compile_c_code(filename, compiler="gcc", standard="c11", output=None):
    if output is None:
        output, ext = os.path.splitext(filename)

    files = [filename] + SOURCE_FILES

    cmd = "{compiler} -std={standard} -o {output} {files} -I include"
    cmd = cmd.format(
        compiler=compiler,
        standard=standard,
        output=output,
        files=" ".join(files),
    )

    assert not subprocess.check_call(cmd.split())
    return output


def compile_py_file(full_path, **kwargs):
    """Wrapper for save_c_code and compile_c_code."""
    node = ast_from_file(full_path)
    c_ast = convert_module(node)
    c_code = str(c_ast)
    c_file = save_c_code(c_code, full_path)
    return compile_c_code(c_file, **kwargs)


def get_args():
    """Standard argument parser function."""
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Python to C converter")

    parser.add_argument("filename", help="Python file to convert.")
    parser.add_argument("-o", "--output", help="Output file.")

    # Compiler options
    parser.add_argument("-c", "--compiler", default="gcc",
                        help="Compiler to use")
    parser.add_argument("--std", default="c11",
                        help="C Standard to use.")

    # Debug options
    parser.add_argument("-p", "--python-ast-dump", action="store_true",
                        default=False,
                        help="Only dump the python ast of the python code.")

    return parser.parse_args()


def main():
    """Program entry point."""
    args = get_args()

    filename = args.filename
    node = ast_from_file(filename)

    if args.python_ast_dump:
        prettyparseprint(node)
        return

    # Generate the c code from the ast
    c_ast = convert_module(node)
    c_code = str(c_ast)

    # Save into c file and compile
    c_file = save_c_code(c_code, filename)
    compile_c_code(c_file, compiler=args.compiler, standard=args.std, output=args.output)

    return


if __name__ == "__main__":
    main()

