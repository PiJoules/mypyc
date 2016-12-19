from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="test_fib",
    ext_modules=cythonize("cyFibo.pyx"),
)
