def func1():
    pass


def func2() -> str:
    return "a"


def func3(a: int, b: long) -> long:
    return a + b


def main(argc: int, argv: [str]) -> int:
    x = func3(2, 5)

    return 0
