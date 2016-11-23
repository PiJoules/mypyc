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

LIB_FILES = [
    "m",
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


def compile_c_code(filename, compiler="gcc", standard="c11"):
    base_name, ext = os.path.splitext(filename)

    files = [filename] + SOURCE_FILES

    cmd = "{compiler} -std={standard} -o {output} {files} -I include"
    cmd = cmd.format(
        compiler=compiler,
        standard=standard,
        output=base_name,
        files=" ".join(files),
    )

    assert not subprocess.check_call(cmd.split())


def get_args():
    """Standard argument parser function."""
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Python to C converter")

    parser.add_argument("filename", help="Python file to convert.")

    # Debug options
    parser.add_argument("-d", "--dump-python-ast", action="store_true",
                        default=False,
                        help="Only dump the python ast of the python code.")

    return parser.parse_args()


def main():
    """Program entry point."""
    args = get_args()

    filename = args.filename
    node = ast_from_file(filename)

    if args.dump_python_ast:
        prettyparseprint(node)
        return

    # Generate the c code from the ast
    c_ast = convert_module(node)
    c_code = str(c_ast)

    # Save into c file and compile
    c_file = save_c_code(c_code, filename)
    compile_c_code(c_file)

    return


if __name__ == "__main__":
    main()

