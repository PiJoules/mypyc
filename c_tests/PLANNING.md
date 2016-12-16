## Objects and Classes

### Referencing
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


from pack import mod.obj
mod.obj.method(arg)

compiles to

#include <pack/mod.h>
mod->obj->method(mod->obj, arg)
```


#### Relative Imports
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


from .pack import mod.obj
pack.obj.method(arg)

compiles to

#include "./pack/mod.h"
mod->obj->method(mod->obj, arg)


from ..pack import mod.obj
mod.obj.method(arg)

compiles to

#include "../pack/mod.h"
mod->obj->method(mod->obj, arg)
```
