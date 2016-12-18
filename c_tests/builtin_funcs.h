#ifndef _BUILTIN_FUNCS_H
#define _BUILTIN_FUNCS_H

#include "mypyc.h"

#define INCREF(obj) obj->ref_count++
#define DECREF(obj) \
    do { \
        obj->ref_count--; \
        if (!(obj->ref_count)){ \
            del((object_t*)obj); \
        } \
    } while(0);

/**
 * obj.method(arg) -> CALL(obj->method, obj, arg) -> obj->method->__exec__(obj, arg)
 * module.func(arg) -> CALL(module->func, arg) -> module->func->__exec__(arg)
 *
 * #define str(...) str_unpack((struct kwargs){.arg1=1, __VA_ARGS__})
 * isinstance(obj, str) -> CALL(isinstance, obj, str) -> isinstance->__exec__(obj, str)  // str stays as the class
 * obj = str(other_obj) -> string_t* obj = CALL(str, other_obj) -> string_t* obj = str->__exec__(other_obj)
 */
#define CALL(func, ...) func->__exec__(__VA_ARGS__)

void mypyc_init();
void mypyc_terminate();

void del(object_t* obj);

void print(object_t* obj);


#endif
