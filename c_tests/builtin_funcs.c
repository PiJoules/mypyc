#include "mypyc.h"

string_object* str(object_object* obj){
    return (string_object*)obj->__str__(obj);
}


void del(void* obj){
    object_object* casted_obj = (object_object*)obj;
    casted_obj->__del__(casted_obj);
}


void print(string_object* obj){
    printf("%s\n", obj->value);
}
