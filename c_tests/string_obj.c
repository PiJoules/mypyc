#include "mypyc.h"

#define CURRENT_OBJ OBJ_NAME(string)

/**
 * Method declarations
 */
static void __init__(CURRENT_OBJ* self);
static string_object* __str__(CURRENT_OBJ* self);

/**
 * Attributes
 */
tuple_object l;

/**
 * The actual object
 */
const CURRENT_OBJ* const string = &(CURRENT_OBJ){
    &l,
    __init__,
    __str__,
};

/**
 * Method definitions
 */

static void __init__(CURRENT_OBJ* self){}

static string_object* __str__(CURRENT_OBJ* self){
    return NULL;
}

