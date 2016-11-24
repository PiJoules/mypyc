#!/usr/bin/env python
# -*- coding: utf-8 -*-


def threes(n: int):
    while n != 1:
        if not (n % 3):
            print(n, 0)
        elif n % 3 == 1:
            print(n, -1)
            n -= 1
        elif n % 3 == 2:
            print(n, 1)
            n += 1
        n //= 3
    print(1)


def main() -> int:
    threes(10)
    return 0


if __name__ == "__main__":
    main()

