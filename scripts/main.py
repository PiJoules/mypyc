#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from pc import Lexer, Parser, CTranslator
from utils import base_arg_parser


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Translate python-esque code to C.")

    parser = base_arg_parser(parser=parser)

    args = parser.parse_args()
    return args


def main():
    """Program entry point"""
    args = get_args()
    filename = args.filename
    lexer = Lexer(filename)
    tokens = lexer.tokens()

    # TODO: Add unit tests for this function
    #tokens = [token for token in lexer]
    #assert tokens == lexer.tokens()

    parser = Parser(tokens)
    parse_tree = parser.parse()

    translator = CTranslator(parse_tree)
    translation = translator.translate()
    print(translation)

    return 0


if __name__ == "__main__":
    main()

