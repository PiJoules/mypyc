#include "mypyc.h"

/**
 * Method declarations
 */
static const string_t string_class;
static string_t* string__exec__(object_t* object, string_t* encoding, string_t* errors);
static const string__init__method_wrapper string__init__;
static const string__del__method_wrapper string__del__;
static const string__str__method_wrapper string__str__;


/**
 * The actual object
 */
static const string_t string_class = {
    .__exec__=string__exec__,
    .props=NULL,

    .ref_count=0,

    .__init__=&string__init__,
    .__del__=&string__del__,
    .__str__=&string__str__,

    .value=NULL,
};

const string_t* const str = &string_class;

static string_t* string__exec__(object_t* object, string_t* encoding, string_t* errors){
    string_t* new_obj = (string_t*)malloc(sizeof(string_t));
    memcpy(new_obj, str, sizeof(string_t));
    INCREF(new_obj);

    CALL(new_obj->__init__, new_obj, object, encoding, errors);

    return new_obj;
}

/**
 * Constructors
 */
string_t* str_literal(char* raw_str){
    string_t* new_str = (string_t*)malloc(sizeof(string_t));
    memcpy(new_str, str, sizeof(string_t));
    INCREF(new_str);

    // Manually malloc and set the value
    size_t len = strlen(raw_str);
    new_str->value = (char*)malloc(len + 1);
    strncpy(new_str->value, raw_str, len);
    new_str->value[len] = '\0';

    return new_str;
}

/**
 * Method definitions
 */

static void __init____call__(string_t* self, object_t* object, string_t* encoding, string_t* errors){
    string_t* obj_str = CALL(object->__str__, object);

    char* str_val = obj_str->value;
    size_t len = strlen(str_val);
    self->value = (char*)realloc(self->value, len + 1);
    strncpy(self->value, str_val, len);
    self->value[len] = '\0';

    DECREF(obj_str);
}

static const string__init__method_wrapper string__init__ = {
    .__exec__=__init____call__,
};

static void __del____call__(string_t* self){
    free(self->value);
}

static const string__del__method_wrapper string__del__ = {
    .__exec__=__del____call__,
};


static string_t* __str____call__(string_t* self){
    return str_literal(self->value);
}

static const string__str__method_wrapper string__str__ = {
    .__exec__=__str____call__,
};


