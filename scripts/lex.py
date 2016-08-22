#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function

from pc.lexer import Lexer
from utils import base_parse_args


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="Print the resulting tokens resulting from a lexical "
        "analysis of the code.")

    args = base_parse_args(parser)
    return args


def main():
    args = get_args()

    filename = args.filename
    lexer = Lexer(filename)
    tokens = lexer.tokens()
    for token in tokens:
        print("{}".format(repr(token)))
    return 0


if __name__ == "__main__":
    main()

