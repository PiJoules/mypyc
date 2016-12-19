# -*- coding: utf-8 -*-

from utils import *

types = {}


def handle_module():
    pass


def main():
    # Comparing n against 2, so n may be an int
    code = """
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
    """

    return 0


if __name__ == "__main__":
    main()

