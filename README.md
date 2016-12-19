# Mypyc: A compiler for the mypy python syntax
In active development


## Requirements
- python 3
- modules
  - cgen
  - nose


## Building
Inside a virtualenv, pip install the dependencies.
```sh
$ pip install -r requirements.txt
```


## Usage
```sh
$ python mypyc.py sample_python_scripts/hello_world.py  # creates sample_python_scripts/hello_world.c and sample_python_scripts/hello_world executable
$ ./sample_python_scripts/hello_world
Hello world
```

## Testing
In the root directory of this repo, run
```sh
$ nosetests
```


## TODO
- Have all conversion functions return a cgen.Generable type
- Handle type inference for assignment before converting the rest of the nodes in a body
- Figure out how to represent multiple tyes with the same variable
- Explore idea of storing wrapper objects inside containers (dicts, sets, lists)
- Implement conversion of control flow
  - with
  - break/continue
  - try/raiseing exceptions
- Reduce number of scoping using parenthesis by not encapsulating function calls or single variables or hardocded types. Only encapsulate expressions with parenthesis.
- Cleanup and modularize c_conversions.py
  - Cleanup the assignment functions
- Tests
  - Add unit tests
  - For `degrees.py`, use assertAlmostEqual to check the floating point outputs
  - Code generation for each integration test sample script
  - Come up with a test that involves assignment not using the test.py script
- Builtin data structures
  - Strings
  - Sets
  - Dictionaries
  - Lists
- Memoize expression type extractions
- Support function types/assignment
- Submit pull request to cgen for adding types

## Timing Comparisons
- https://fengmk2.com/blog/2011/fibonacci/nodejs-python-php-ruby-lua.html
- http://notes-on-cython.readthedocs.io/en/latest/fibo_speed.html
