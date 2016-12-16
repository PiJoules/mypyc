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

