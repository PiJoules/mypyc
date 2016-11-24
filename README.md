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
- Implement conversion of control flow
  - while
  - with
- Reduce number of scoping using parenthesis by not encapsulating function calls or single variables or hardocded types. Only encapsulate expressions with parenthesis.
- Cleanup and modularize c_conversions.py
- Tests
  - Add unit tests
  - For `degrees.py`, use assertAlmostEqual to check the floating point outputs
