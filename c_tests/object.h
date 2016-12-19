#ifndef _OBJECT_H
#define _OBJECT_H


typedef struct object__init__method_wrapper object__init__method_wrapper;
struct object__init__method_wrapper {
    void (*__exec__)(object_t* self);
    METHOD_WRAPPER_ATTRS
};

typedef struct object__del__method_wrapper object__del__method_wrapper;
struct object__del__method_wrapper {
    void (*__exec__)(object_t* self);
    METHOD_WRAPPER_ATTRS
};

typedef struct object__str__method_wrapper object__str__method_wrapper;
struct object__str__method_wrapper {
    string_t* (*__exec__)(object_t* self);
    METHOD_WRAPPER_ATTRS
};

typedef struct object__int__method_wrapper object__int__method_wrapper;
struct object__int__method_wrapper {
    int_t* (*__exec__)(object_t* self);
    METHOD_WRAPPER_ATTRS
};

struct object_t {
    object_t* (*__exec__)();

    class_properties* props;

    // Props
    size_t ref_count;

    // Methods
    const object__init__method_wrapper* __init__;
    const object__del__method_wrapper* __del__;
    const object__str__method_wrapper* __str__;
    const object__int__method_wrapper* __int__;
};

extern const object_t* const object;

#endif
