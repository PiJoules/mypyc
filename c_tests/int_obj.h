#ifndef _INT_OBJ_H
#define _INT_OBJ_H


typedef struct int__init__method_wrapper int__init__method_wrapper;
struct int__init__method_wrapper {
    void (*__exec__)(int_t* self, object_t* x, int_t* base);
    METHOD_WRAPPER_ATTRS
};

typedef struct int__del__method_wrapper int__del__method_wrapper;
struct int__del__method_wrapper {
    void (*__exec__)(int_t* self);
    METHOD_WRAPPER_ATTRS
};

typedef struct int__str__method_wrapper int__str__method_wrapper;
struct int__str__method_wrapper {
    string_t* (*__exec__)(int_t* self);
    METHOD_WRAPPER_ATTRS
}
;
typedef struct int__int__method_wrapper int__int__method_wrapper;
struct int__int__method_wrapper {
    int_t* (*__exec__)(int_t* self);
    METHOD_WRAPPER_ATTRS
};

struct int_t {
    int_t* (*__exec__)(object_t* x, int_t* base);

    class_properties* props;

    // Props
    size_t ref_count;

    // Methods
    const int__init__method_wrapper* __init__;
    const int__del__method_wrapper* __del__;
    const int__str__method_wrapper* __str__;
    const int__int__method_wrapper* __int__;

    long value;
};

int_t* int_literal(long value);

extern const int_t* const integer;

#endif
