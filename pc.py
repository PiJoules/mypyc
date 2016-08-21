#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from lexer import Lexer
from parser import Parser
from c_translator import CTranslator

import sys
import json
import logging

LOGGER = logging.getLogger(__name__)


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Translate and compile pc code")

    parser.add_argument("filename", help=".pc file to compile.")

    # Logging/debugging
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Logging verbosity. More verbose means more "
                        "logging info.")
    parser.add_argument("--lex", action="store_true", default=False,
                        help="Just print the tokens resulting from a lexical "
                        "analysis of the code.")
    parser.add_argument("--parse", action="store_true", default=False,
                        help="Just print the resulting parse tree in JSON.")

    args = parser.parse_args()

    # Configure logger
    logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s",
                        stream=sys.stderr)
    if args.verbose == 1:
        LOGGER.setLevel(logging.INFO)
    elif args.verbose == 2:
        LOGGER.setLevel(logging.DEBUG)

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

    if args.lex:
        for token in tokens:
            print("'{}'".format(repr(token)))
        return 0

    parser = Parser(tokens)
    parse_tree = parser.parse()
    if args.parse:
        print("Parse tree")
        print(json.dumps(parse_tree.json(), indent=4))
        print("")
        return 0

    translator = CTranslator(parse_tree)
    translation = translator.translate()
    print(translation)

    return 0


if __name__ == "__main__":
    main()

