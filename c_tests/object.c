#include "mypyc.h"


/**
 * Declarations
 */
static const object_t object_class;
static object_t* object__exec__();
static const object__init__method_wrapper object__init__;
static const object__del__method_wrapper object__del__;
static const object__str__method_wrapper object__str__;


/**
 * Base object class
 */
static const object_t object_class = {
    .__exec__=object__exec__,
    .props=NULL,

    .ref_count=0,

    .__init__=&object__init__,
    .__str__=&object__str__,
    .__del__=&object__del__,
};

const object_t* const object = &object_class;


/**
 * Methods
 */
static object_t* object__exec__(){
    object_t* new_obj = (object_t*)malloc(sizeof(object_t));
    memcpy(new_obj, object, sizeof(object_t));
    INCREF(new_obj);
    CALL(new_obj->__init__, new_obj);
    return new_obj;
}

static void __init____call__(object_t* self){}

static const object__init__method_wrapper object__init__ = {
    .__exec__=__init____call__,
};

static void __del____call__(object_t* self){}

static const object__del__method_wrapper object__del__ = {
    .__exec__=__del____call__,
};


static string_t* __str____call__(object_t* self){
    return str_literal("object");
}

static const object__str__method_wrapper object__str__ = {
    .__exec__=__str____call__,
};


