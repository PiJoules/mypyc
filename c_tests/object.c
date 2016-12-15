#include "mypyc.h"


/**
 * Method declarations
 */
static void __init__(object_object* self);
static string_object* __str__(object_object* self);


/**
 * Attributes
 */
tuple_object l;


/**
 * The actual object
 */
const object_object* const object = &(object_object){
    &l,
    __init__,
    __str__,
};


/**
 * Method definitions
 */

static void __init__(object_object* self){}

static string_object* __str__(object_object* self){
    return NULL;
}

