#!/usr/bin/env python
# -*- coding: utf-8 -*-


def remove_char_from_string(s: str, c: str) -> str:
    return s.replace(c, "")


def main() -> int:
    print(remove_char_from_string("Hello world!", "o"))
    print(remove_char_from_string("Not creative example", "z"))
    return 0


if __name__ == "__main__":
    main()

