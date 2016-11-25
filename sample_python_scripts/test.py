def func1():
    pass


def func2() -> str:
    return "a"


def func3(a: int, b: int) -> int:
    return a + b


def main(argc: int, argv: [str]) -> int:
    x = func3(2, 5)
    print(x)
    return 0


if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)

