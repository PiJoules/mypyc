#ifndef _STRING_OBJ_H
#define _STRING_OBJ_H

typedef struct string__init__method_wrapper string__init__method_wrapper;
struct string__init__method_wrapper {
    void (*__exec__)(string_t* self, object_t* object, string_t* encoding, string_t* errors);
    METHOD_WRAPPER_ATTRS
};

typedef struct string__del__method_wrapper string__del__method_wrapper;
struct string__del__method_wrapper {
    void (*__exec__)(string_t* self);
    METHOD_WRAPPER_ATTRS
};

typedef struct string__str__method_wrapper string__str__method_wrapper;
struct string__str__method_wrapper {
    string_t* (*__exec__)(string_t* self);
    METHOD_WRAPPER_ATTRS
};

struct string_t {
    string_t* (*__exec__)(object_t* object, string_t* encoding, string_t* errors);

    class_properties* props;

    // Props
    size_t ref_count;

    // Methods
    const string__init__method_wrapper* __init__;
    const string__del__method_wrapper* __del__;
    const string__str__method_wrapper* __str__;

    char* value;
};

string_t* str_literal(char* str);

extern const string_t* const str;

const object_t* str_default_kwarg_object;
const string_t* str_default_kwarg_encoding;
const string_t* str_default_kwarg_errors;

#endif
