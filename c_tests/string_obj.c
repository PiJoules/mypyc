#include "mypyc.h"

/**
 * Method declarations
 */
static void __init__(string_t* self, char* str);
static void __del__(string_t* self);
static string_t* __str__(string_t* self);

/**
 * Attributes
 */
static class_properties _props = {
};

/**
 * The actual object
 */
static const string_t* const string_class = &(string_t){
    .props=NULL,

    .ref_count=0,

    .__init__=__init__,
    .__del__=__del__,
    .__str__=__str__,

    .value=NULL,
};

/**
 * Constructors
 */
string_t* str(struct str_kwargs kwargs){
    return str_base(kwargs.object, kwargs.encoding, kwargs.errors);
}

string_t* str_base(object_t* object, object_t* encoding, object_t* errors){
    return object->__str__(object);
}

string_t* str_literal(char* str){
    string_t* new_str = (string_t*)malloc(sizeof(string_t));
    memcpy(new_str, string_class, sizeof(string_t));
    INCREF(new_str);

    new_str->__init__(new_str, str);
    return new_str;
}

/**
 * Method definitions
 */

static void __init__(string_t* self, char* str){
    size_t len = strlen(str);
    self->value = (char*)malloc(len + 1);
    strncpy(self->value, str, len);
    self->value[len] = '\0';
}

static void __del__(string_t* self){
    free(self->value);
    free(self);
}

static string_t* __str__(string_t* self){
    return self;
}

