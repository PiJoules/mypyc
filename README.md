# Mypyc: A compiler for the mypy python syntax
In active development


## Requirements
- python 3
- modules
  - cgen
  - nose


## Usage
```
$ python mypyc.py sample_python_scripts/hello_world.py  # creates sample_python_scripts/hello_world.c and sample_python_scripts/hello_world executable
$ ./sample_python_scripts/hello_world
Hello world
```

## Testing
In the root directory of this repo, run
```
$ nosetests
```


## TODO
- Implement conversion of control flow
  - while
  - with
- Reduce number of scoping using parenthesis by not encapsulating function calls or single variables or hardocded types. Only encapsulate expressions with parenthesis.
- Cleanup and modularize c_conversions.py
- Tests
  - Add unit tests
  - For `degrees.py`, use assertAlmostEqual to check the floating point outputs
