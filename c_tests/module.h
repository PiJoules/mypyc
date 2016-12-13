#ifndef _MODULE_H
#define _MODULE_H

/**
 * Header for exposing a module, whose name is "module"
 */


typedef struct module_module module_module;
struct module_module {
    /**
     * Contents in the module
     */

    // Constants
    float f;
    int i;
    char c;

    // Free functions
    void (*func1)();
    char* (*func2)(int i);

    // Classes


    // Other modules


};

// Module to use
extern const module_module* const module;


#endif
