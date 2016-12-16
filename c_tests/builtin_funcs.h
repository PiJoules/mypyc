#ifndef _BUILTIN_FUNCS_H
#define _BUILTIN_FUNCS_H

#include "mypyc.h"

/**
 * def new(self, arg1, arg2, kwarg1=val1, kwarg2=val2, *args, **kwargs)
 * func call: new(object, arg1, arg2, .kwarg1=1, kwarg2=2, kwarg3=3)
 */
//object_object* new(object_object* self, tuple_object* varargs, dict_object* kwargs);


string_object* str(object_object* obj);

void del(void* obj);


void print(string_object* obj);


#endif
