#include "mypyc.h"
#include "module.h"


/**
 * Contents of module
 */

/**
 * Constants defined in the module cannot be defined as constant variables that are then
 * initialized in the struct. Either macros should be used or these should be hardcoded
 * into the struct initialization.
 *
 * Add __CONST__ to make sure that this macro does not conflict with any variables.
 * TODO: Find better way to allow for setting constant values.
 */
#define f__CONST__ 3.14
#define i__CONST__ 3
#define c__CONST__ 'A'


/**
 * Free functions
 */
void (*func1)();
char* (*func2)(int i);


// Module definition
const module_module* const module = &(module_module){
    3.14,
    3,
    'A',
};
