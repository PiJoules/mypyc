#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def long_description():
    with open("README.md", "r") as readme:
        return readme.read()


def packages():
    return find_packages(include=["pc*", "scripts*"])


def install_requires():
    with open("requirements.txt", "r") as requirements:
        return requirements.readlines()


setup(
    name="pc",
    version="0.0.1",
    description="Python to C",
    long_description=long_description(),
    url="https://github.com/PiJoules/pc",
    author="Leonard Chan",
    author_email="lchan1994@yahoo.com",
    license="Unlicense",
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    keywords="python, c",
    packages=packages(),
    install_requires=install_requires(),
    test_suit="nose.collector",
    entry_points={
        "console_scripts": [
            "pc=scripts.main:main",
            "parse=scripts.parse:main",
        ],
    },
)
