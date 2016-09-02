# Python to C
Convert python-esque code to C.

## Setup
Create and install the project as a package in a virtual environment.
```sh
$ virtualenv pc  # Create the venv
$ source pc/bin/activate  # Activate the venv
(pc) $ ./setup.sh  # Builds and installs the package
```

## Usage
Compiling
```sh
(pc) $ pc samples/hello_world.pc
(pc) $ ./samples/hello_world
Hello world
```

Print the translated C code.
```sh
(pc) $ pc samples/hello_world.pc -p
int main(int argc, char** argv){
    printf("%s\n", "Hello world");
    return 0;
}
```

## TODO
- Formalizing parsing method
  - Make each rule method in the parse a class instead that inherits from a Rule class.
