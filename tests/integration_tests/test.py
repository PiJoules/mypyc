# -*- coding: utf-8 -*-

import unittest
import os
import subprocess

import mypyc


# This script must be called from the base dir of the repo
SAMPLE_SCRIPTS_PATH = os.path.join(os.getcwd(), "sample_python_scripts")
EXPECTED_OUTPUT_DIR = os.path.join(os.getcwd(), "tests/integration_tests/expected_outputs")


class IntegrationTests(unittest.TestCase):
    def __check_output(self, filename):
        """Generate the output file from the python filename (eg. hello_world.py)."""
        full_path = os.path.join(SAMPLE_SCRIPTS_PATH, filename)
        exe_file = mypyc.compile_py_file(full_path)

        base_name, ext = os.path.splitext(filename)
        expected_file = os.path.join(EXPECTED_OUTPUT_DIR, base_name + ".expected")
        output_file = os.path.join(EXPECTED_OUTPUT_DIR, base_name + ".output")

        with open(output_file, "wb") as f:
            f.write(subprocess.check_output([exe_file]))

        self.__assert_equal_files(output_file, expected_file)

    def __assert_equal_files(self, file1, file2):
        with open(file1, "r") as f1, open(file2, "r") as f2:
            line1 = next(f1, None)
            line2 = next(f2, None)
            while line1 or line2:
                self.assertEqual(line1, line2)
                line1 = next(f1, None)
                line2 = next(f2, None)

    def test_hello_world(self):
        self.__check_output("hello_world.py")

    def test_degrees(self):
        self.__check_output("degrees.py")

    def test_fizzbuzz(self):
        self.__check_output("fizzbuzz.py")

    def test_game_of_threes(self):
        self.__check_output("game_of_threes.py")

    def test_test(self):
        """Not a real test script. Just temporarily here to test variable assignment."""
        self.__check_output("test.py")

