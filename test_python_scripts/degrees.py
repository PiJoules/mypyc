#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


def degrees_to_radians(degrees: float) -> float:
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    return math.degrees(radians)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    pass


def celsius_to_fahrenheit(celsius: float) -> float:
    pass


def celsius_to_kelvin(celsius: float) -> float:
    pass


def kelvin_to_celsius(kelvin: float) -> float:
    pass


def main(argc: int, argv: [str]) -> int:
    print("180 deg to radians:", degrees_to_radians(180.0))
    print("hardcoded 3.14159 to degrees:", radians_to_degrees(3.14159))
    print("builtin math.pi to degrees:", radians_to_degrees(math.pi))
    return 0


if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)

