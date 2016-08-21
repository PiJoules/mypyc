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
Just prints the translated C code for now
```sh
(pc) $ pc samples/hello_world.pc
int main(int argc, char** argv){
    printf("%s\n", "Hello world");
    return 0;
}
```

## TODO
...
