#include "mypyc.h"

/**
 * Method declarations
 */
static const int_t string_class;
static int_t* int__exec__(object_t* x, int_t* base);
static const int__init__method_wrapper int__init__;
static const int__del__method_wrapper int__del__;
static const int__str__method_wrapper int__str__;
static const int__int__method_wrapper int__int__;


/**
 * The actual object
 */
static const int_t int_class = {
    .__exec__=int__exec__,
    .props=NULL,

    .ref_count=0,

    .__init__=&int__init__,
    .__del__=&int__del__,
    .__str__=&int__str__,
    .__int__=&int__int__,
    .value=0,
};

const int_t* const integer = &int_class;

static int_t* int__exec__(object_t* x, int_t* base){
    int_t* new_obj = (int_t*)malloc(sizeof(int_t));
    memcpy(new_obj, integer, sizeof(int_t));
    INCREF(new_obj);

    CALL(new_obj->__init__, new_obj, x, base);

    return new_obj;
}

/**
 * Constructors
 */
int_t* int_literal(long value){
    int_t* new_obj = (int_t*)malloc(sizeof(int_t));
    memcpy(new_obj, integer, sizeof(int_t));
    INCREF(new_obj);

    // Manually set the value
    new_obj->value = value;

    return new_obj;
}

/**
 * Method definitions
 */

static void __init____call__(int_t* self, object_t* x, int_t* base){
    int_t* obj = CALL(object->__int__, x);

    // Set the value
    self->value = obj->value;

    DECREF(obj);
}

static const int__init__method_wrapper int__init__ = {
    .__exec__=__init____call__,
};

static void __del____call__(int_t* self){}

static const int__del__method_wrapper int__del__ = {
    .__exec__=__del____call__,
};


static string_t* __str____call__(int_t* self){
    char buff[256];
    sprintf(buff, "%ld", self->value);
    return str_literal(buff);
}

static const int__str__method_wrapper int__str__ = {
    .__exec__=__str____call__,
};

static int_t* __int____call__(int_t* self){
    return int_literal(self->value);
}

static const int__int__method_wrapper int__int__ = {
    .__exec__=__int____call__,
};


