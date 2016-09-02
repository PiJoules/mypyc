#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from pc import Lexer, Parser, CTranslator
from utils import base_parse_args

import subprocess
import os


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Translate python-esque code to C.")

    # C arguments
    parser.add_argument("-c", "--compiler", default="gcc",
                        help="Compiler to use.")
    parser.add_argument("--std", default="c99",
                        help="C standard.")
    parser.add_argument("-o", "--output", type=str,
                        help="Output executable name.")

    parser.add_argument("-p", "--print", action="store_true", default=False,
                        help="Just print the c code.")

    args = base_parse_args(parser)
    return args


def main():
    """Program entry point"""
    args = get_args()
    filename = args.filename

    parser = Parser(filename)
    parse_tree = parser.parse()

    translator = CTranslator(parse_tree)
    translation = translator.translate()
    if args.print:
        print(translation)
        return 0

    # Save into c file and compile it
    base_name, ext = os.path.splitext(filename)
    c_file = base_name + ".c"
    with open(c_file, "w") as f:
        f.write(translation)

    cmd = "{compiler} -std={standard} -o {output} {files}"
    cmd = cmd.format(
        compiler=args.compiler,
        standard=args.std,
        output=base_name,
        files=" ".join([c_file])
    )
    assert not subprocess.check_call(cmd.split())

    return 0


if __name__ == "__main__":
    main()

