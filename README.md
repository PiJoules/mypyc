# Mypyc: A compiler for the mypy python syntax
In active development


## Requirements
- python 3
- cgen module


## Usage
```
$ python mypyc.py test_python_scripts/hello_world.py  # creates test_python_scripts/hello_world.c and test_python_scripts/hello_world executable
$ ./test_python_scripts/hello_world
Hello world
```

## TODO
- Implement conversion of control flow
  - while
  - with
- Reduce number of scoping using parenthesis by not encapsulating function calls or single variables or hardocded types. Only encapsulate expressions with parenthesis.
- Cleanup and modularize c_conversions.py
