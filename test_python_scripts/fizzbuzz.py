#!/usr/bin/env python
# -*- coding: utf-8 -*-


def fizzbuzz(n: int):
    for i in range(1, n+1):
        if not i % 3 and not i % 5:
            print("fizzbuzz")
        elif not i % 3:
            print("fizz")
        elif not i % 5:
            print("buzz")
        else:
            print(i)


def main(argc: int, argv: [str]) -> int:
    fizzbuzz(15)
    return 0


if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)

