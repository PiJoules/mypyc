#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


def degrees_to_radians(degrees: float) -> float:
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    return math.degrees(radians)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


def celsius_to_fahrenheit(celsius: float) -> float:
    return 9 * celsius / 5 + 32


def celsius_to_kelvin(celsius: float) -> float:
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    return kelvin - 273.15


def main(argc: int, argv: [str]) -> int:
    print("180 deg to radians:", degrees_to_radians(180))
    print("hardcoded 3.14159 to degrees:", radians_to_degrees(3.14159))
    print("builtin math.pi to degrees:", radians_to_degrees(math.pi))
    print("-40 deg fahrenheit to celsius:", fahrenheit_to_celsius(-40))
    print("-459.67 deg fahrenheit to celsius:", fahrenheit_to_celsius(-459.67))
    print("-40 deg celsius to fahrenheit:", celsius_to_fahrenheit(-40))
    print("0 deg celsius to kelvin:", celsius_to_kelvin(0))
    print("0 deg kelvin to celsius:", kelvin_to_celsius(0))
    return 0


if __name__ == "__main__":
    import sys
    main(len(sys.argv), sys.argv)

