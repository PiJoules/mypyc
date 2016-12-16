#include "mypyc.h"


/**
 * Method declarations
 */
static void __init__(object_object* self);
static void __del__(object_object* self);
static string_object* __str__(object_object* self);


/**
 * Attributes
 */
static class_properties _props = {
};


/**
 * The actual object
 */
const object_object* const object = &(object_object){
    .props=NULL,

    .__init__=__init__,
    .__str__=__str__,
    .__del__=__del__,
};


/**
 * Method definitions
 */

static void __init__(object_object* self){
    printf("object __init__\n");
}
static void __del__(object_object* self){
    printf("object del\n");
}

static string_object* __str__(object_object* self){
    return new_string("object");
}

