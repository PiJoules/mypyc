#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main(argc: int, argv: [str]) -> int:
    print("Hello world")
    return 0

if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)

