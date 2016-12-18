#include "mypyc.h"


static const object_t object_class;


/**
 * Methods
 */
static void __init____call__(object_t* self){}

static const object_t object__init__ = {
    .__exec__=__init____call__,
};

static void __del____call__(object_t* self){}

static const object_t object__del__ = {
    .__exec__=__del____call__,
};


static string_t* __str____call__(object_t* self){
    return str_literal("object");
}

static const object_t object__str__ = {
    .__exec__=__str____call__,
};


static object_t* object__exec__(){
    object_t* new_obj = (object_t*)malloc(sizeof(object_t));
    memcpy(new_obj, &object_class, sizeof(object_t));
    INCREF(new_obj);
    CALL(new_obj->__init__);
    return new_obj;
}

object_t obj;


/**
 * Attributes
 */
static class_properties _props = {
};


/**
 * The actual object_class
 */
static const object_t object_class = {
    .props=NULL,

    .ref_count=0,

    .__exec__=object__exec__,
    .__init__=&object__init__,
    .__str__=&object__str__,
    .__del__=&object__del__,
};


/**
 * Constructors
 */
//object_t* object(){
//    object_t* new_obj = (object_t*)malloc(sizeof(object_t));
//    memcpy(new_obj, object_class, sizeof(object_t));
//    INCREF(new_obj);
//    //new_obj->__init__(new_obj);
//    return new_obj;
//}


/**
 * Method definitions
 */

//static void __init__(object_t* self){}
//static void __del__(object_t* self){}

//static string_t* __str__(object_t* self){
//    return str_literal("object_class");
//}

