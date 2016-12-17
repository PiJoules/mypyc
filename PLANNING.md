## Objects and Classes
Objects will be represented by structs that contain methods, attributes, and class properties.

### Class Structure
Classes will be structs containing 3 nested structs.

```
struct {object}_t {
    class_properties props;
    ...
    Properties/methods
    ...
};
```

Where `class_properties` is another struct that all classes share and is predefined. This will contain info about the class that is set at compile time and will be available at runtime.


### Methods and Properties
All methods and properties are scattered in the class in no particular order, as long as all the methods and properties retain the same order when inheriting from another class and all properties and methods are of the same size. The size part is accomplished by having all methods be pointers and the order of the properties is maintained by the python to c compiler.


### Inheritance and Overriding
Custom defined classes that inherit or override methods have their attributes tracked by the compiler to retain the order. Any overrides in methods are also tracked by the compiler, keeping the order of methods the same, but chaning the return type and arguments approproately.


### Compile Time Class Definition
Classes for now will be created at compile time instead of runtime as in python. The consequences of this include the "__new__" method not being evaluated at runtime as it normally would in python. This could possibly be alieviated by running the code in python space during the compiling of python to c to attempt to evaluate the __new__ code before c compilation.


## Arguments
Arguments are either positional or keyword arguments. Functions are able to accept a finite of positional/keyword args unless they choose to add *args and **kwargs to the function definition. In this case, they can take an unlimited amount of positional or keyword args that are available to the function as a tuple of args and a dict respectively. Extra positional args are given in the tuple and extra keyword args are given in the dict.

To alleviate variable positional arguments, all function calls will end with an object that indicates the end of an argument if it accepts variable arguments. For this, a check will need to be done to see if the function takes variable arguments.


### Only Positional
```
def func(arg1, arg2):
    pass

func(1, 2)

compiles to

void func(int arg1, int arg2){}
func(1, 2)
```

### Only Keyword
```
def func(arg1=1, arg2=2):
    pass

func(arg2=3)

compiles to

#define func(...) func_unpack((struct func_kwargs){.arg1=1, .arg2=2, __VA_ARGS__})
void func_unpack(struct func_kwargs kwargs){
    return func_base(kwargs.arg1, kwargs.arg2);
}
void func_base(int arg1, int arg2){}
func1(.arg2=3)
```


### Both
```
def func(arg1, arg2, arg3=1, arg4=2):
    pass

func(val1, val2, arg4=4)

compiles to

#define func(arg1, arg2, ...) func_unpack(arg1, arg2, (struct func_kwargs){.arg3=1, .arg4=2, __VA_ARGS__})
void func_unpack(int arg1, int arg2, struct kwargs kwargs){
    return func_base(arg1, arg2, kwargs.arg3, kwargs.arg4);
}
void func_base(int arg1, int arg2, int arg3, int arg4){}
func(val1, val2, .arg4=4)
```


### Extra Positional (Variable Args)
Since starred arguments can be mixed with variable arguments passed to a function call, all positional arguments will need to be packed into a tuple, then unpacked into the actual arguments.

The VAR_ARGS_START is inserted at the position where the positional and keyword arguments end. This can be determined in the ast. The VAR_ARGS_END is placed at the end of the funciton call.
The VAR_ARGS_START is required in case the function has no other positional arguments and only contains variable arguments.

```
def func(arg1, arg2, *args):
    # Able to access args as a tuple
    pass

func(1, 2, 3, 4)

compiles to


// Compiler library function
tuple_t* new_tuple_from_va_list(va_list args){
    // Creates a tuple of objects up until VAR_ARGS_END is found
    object_t* obj = va_arg(args, object_t*);
    list_t* lst = empty_list();
    while (obj != VAR_ARGS_END){
        if (obj == starred){
            lst.merge(obj);
        }
        else {
            lst->append(obj);
        }
        obj = va_arg(args, object_t*);
    }
    return new_tuple(lst);
}

void func(va_start_t* args_start, ...){
    # Create tuple from va_list
    va_list args;
    va_start(args, args_start);
    tuple_t* tup_args = new_tuple_from_va_list(args);
    va_end(args);
    return func_base(tup_args.get(0), tup_args.get(1), tup_args.slice(2));
}
void func_base(int arg1, int arg2, tuple_t* args){}
func(VAR_ARGS_START, 1, 2, 3, 4, VAR_ARGS_END)
```

### Starred Args
Will need to check on the python ast for the version since the call args change between 3.4 and 3.5.
Check greensnakes for the documentation for the function Call node.

```
def func(arg1, arg2, *args):
    # Able to access args as a tuple
    pass

func(1, 2, 3, 4, *(5, 6, 7))

compiles to

void func_base(int arg1, int arg2, tuple_t* args){}
func(VAR_ARGS_START, 1, 2, 3, 4, starred(new_tuple(VAR_ARGS_START, 5, 6, 7, VAR_ARGS_END)), VAR_ARGS_END)


func(*(1, 2, 3))

compiles to

void func_base(int arg1, int arg2, tuple_t* args){}
func(VAR_ARGS_START, starred(1, 2, 3), VAR_ARGS_END)
```


### Extra Keyword
The kwargs will need to be packed into a dictionary if variable keyword arguments are accepted in the function

```
def func(arg1=1, arg2=2, **kwargs):
    # Able to access kwargs as a dict
    pass

func(arg4=10, arg2=3)  # Order does not matter for keyword args

compiles to

// Compiler library function
dict_t* new_dict_from_va_list(va_list args){
    // Creates a dict of objects up until VAR_ARGS_END is found
    object_t* obj = va_arg(args, object_t*);
    dict_t* d = empty_dict();
    while (obj != VAR_ARGS_END){
        if (obj == double_starred){
            d->merge_inplace(d, obj);
        }
        else {
            dict_item_t* item = (dict_item_t*)obj;
            d->insert(d, item->key, item->value);
        }
        obj = va_arg(args, object_t*);
    }
    return d;
}

#define DICT_ITEM(key, val) new_dict_item(key, val)
void func(va_start_t* args_start, ...){
    va_list args;
    va_start(args, args_start);
    dict_t* d_passed = new_dict_from_va_list(args);
    // default_args is a dictionary made beforehand that contains the default values of the args
    dict_t* d = default_args->merge(default_args, d_passed);
    va_end(args);
    return func_base(d.pop("arg1"), d.pop("arg2"), d);
}
void func_base(int arg1, int arg2, dict_t* kwargs){}
func(VAR_ARGS_START, DICT_ITEM("arg4", 10), DICT_ITEM("arg2", 3), VAR_ARGS_END);
```

### All Arg Types
```
def func(arg1, arg2, arg3=1, arg4=2, *args, **kwargs):
    pass
func(1, 2, arg3=3, arg4=4, *(1, 2, 3), **{"arg5": 5, "arg6": 6})

compiles to


// Wrapper for variable argument signs starting with VAR_ARGS_START and VAR_ARGS_END
#define VAR_ARGS(...) VAR_ARGS_START, __VA_ARGS__, VAR_ARGS_END
#define DICT_ITEM(key, val) new_dict_item(key, val)
// pack_args wraps the container in a special class for holding packed variable positional args
// pack_kwargs wraps the dictionary in a special class for holding packed variable keyword args
void func(va_start_t* start, ...){
    va_list args_list;
    va_start(args_list, start);

    // default_kwargs is a dictionary created beforehand that contains the default argument values
    list_t* temp_lst = empty_list();
    dict_t* kwargs = empty_dict();
    object_t* obj = va_arg(args, object_t*);
    while (obj != VAR_ARGS_END){
        if (isinstance(obj, packed_args)){
            temp_lst->merge_inplace(temp_lst, ((packed_args_t*)obj)->container);
        }
        else if (isinstance(obj, packed_kwargs)){
            kwargs->extend(kwargs, ((packed_kwargs_t*)obj)->container);
        }
        else if (isinstance(obj, dict_item)){
            dict_item_t* item = (dict_item_t*)obj;
            d->insert(d, item->key, item->value);
        }
        else {
            // Positional argument
            temp_lst->append(temp_lst, obj);
        }
        obj = va_arg(args, object_t*);
    }

    va_end(args_list);

    // The pop methods removes the element at the index specified by the first argument
    // and returns the second argument if the index is not in the container.
    tuple_t* args = tuple(temp_lst);
    return func_base(args.pop(0), args.pop(1),
        kwargs.pop("arg3", args.pop(2, 1)),
        kwargs.pop("arg4", args.pop(3, 2)),
        args, kwargs
    );
}
void func_base(int arg1, int arg2, int arg3, int arg4, tuple_t* args, dict_t* kwargs){}
func(VAR_ARGS(1, 2, DICT_ITEM("arg3", 3), DICT_ITEM("arg4", 4), pack_args(new_tuple(VAR_ARGS(1, 2, 3))), pack_kwargs(new_dict(VAR_ARGS(DICT_ITEM("arg5", 5), DICT_ITEM("arg6", 6))))))
```



## Referencing
All periods in python representing calling a method or referenceing an object in another object will be replaced by pointer dereferencing.

Example:
```
myobj.method(arg)

compiles to

myobj->method(myobj, arg)


module.class.property.method(arg)

compiles to

module->class->property->method(module->class->property, arg)
```

### Imports
Imports will be replace by `include` macros where only the top level import is included, but the package itself is represented with nested header and source files where the header files are constantly edited to expose whatever is represented by the import statement.

#### Modules
Modules are whole .c files exposed with a corresponding .h file. The header exposes a module object. When importing, the import is replaced with an include of this header which is prefixed with "module_" and postfixed with ".h"

```
import mod
mod.object.method(a)

compiles to

#include <module_mod.h>
mod->object->method(mod->object, a)

where module_mod.h contains an object called `mod` that contains all objects declared in it.
```


#### Packages
Packages just have the root level of the package imported, represented as "package_{package_name}.h". Depending on what modules are imported as python determines what the package object inside this header exposes.

```
import pack.nested_pack.mod
pack.nested_pack.mod.obj.method(arg)

compiles to

#include <package_pack.h>
pack->nested_pack->mod->obj->method(pack->nested_pack->nod->obj, arg)

where package_pack.h exposes the nested_pack object in "pack/nested_pack.h" where nested_pack exposes the mod object in "pack/nested_pack/mod.h" which in turn only exposes `obj`.
```


#### Import From
This exposes any nested object, packages, or modules by spelling out the full path in the include macro.

```
from mod import obj
obj.method(arg)

compiles to

#include <mod/obj.h>
obj->method(obj, arg)


from pack.mod import obj
obj.method(arg)

compiles to

#include <pack/mod/obj.h>
obj->method(obj, arg)


from pack import mod
mod.obj.method(arg)

compiles to

#include <pack/mod.h>
mod->obj->method(mod->obj, arg)
```


### Relative Imports
Imports starting with . or .. represent relative imports in which case, the include macro will use double quotes instead of triangle brackets.

```
from .mod import obj
obj.method(arg)

compiles to

#include "./mod/obj.h"
obj->method(obj, arg)


from .pack.mod import obj
obj.method(arg)

compiles to

#include "./pack/mod/obj.h"
obj->method(obj, arg)


from .pack import mod
pack.obj.method(arg)

compiles to

#include "./pack/mod.h"
mod->obj->method(mod->obj, arg)


from ..pack import mod
mod.obj.method(arg)

compiles to

#include "../pack/mod.h"
mod->obj->method(mod->obj, arg)
```


### Import As
Rules are same as the previously defined import rules, but a new object is created of the same type that is renamed to the `as` target.


```
from mod import obj as obj2
obj2.method(arg)

compiles to

#include <mod/obj.h>
obj_type obj2 = obj;
obj2->method(obj2, arg)


from pack.mod import obj as obj2
obj2.method(arg)

compiles to

#include <pack/mod/obj.h>
obj_type obj2 = obj;
obj2->method(obj2, arg)


import pack.nested_pack.mod as mod2
mod2.obj.method(arg)

compiles to

#include <package_pack.h>
mod_type mod2 = pack->nested_pack->mod;
mod2->obj->method(pack->nested_pack->nod->obj, arg)
```

