#include "mypyc.h"
#include "module.h"


/**
 * Contents of module
 */

/**
 * Constants defined in the module cannot be defined as constant variables that are then
 * initialized in the struct. Either macros should be used or these should be hardcoded
 * into the struct initialization.
 */


/**
 * Free functions
 */
void func1();
char* func2(int i);


// Module definition
const module_module* const module = &(module_module){
    .c='A',
    .f=3.14,
    .i=3,
    .func1=func1,
    .func2=func2,
    .c='B',
};


/**
 * Free function definitions
 */

void func1(){}


char* func2(int i){
    return "\n";
}

