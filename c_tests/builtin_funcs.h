#ifndef _BUILTIN_FUNCS_H
#define _BUILTIN_FUNCS_H

#include "mypyc.h"

#define INCREF(obj) obj->ref_count++
#define DECREF(obj) \
    do { \
        obj->ref_count--; \
        if (!(obj->ref_count)){ \
            del(obj); \
        } \
    } while(0);

#define CALL(func, ...) func->__exec__(__VA_ARGS__)

void del(object_t* obj);

void print(string_t* obj);


#endif
