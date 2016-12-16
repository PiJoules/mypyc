#include "mypyc.h"

string_object* str(object_object* obj){
    return (string_object*)obj->__str__(obj);
}


void del(void* obj){
    printf("del func called\n");
    object_object* casted_obj = (object_object*)obj;
    printf("obj addr: %p\n", obj);
    printf("casted_obj addr: %p\n", casted_obj);
    casted_obj->__del__(casted_obj);
    printf("deleted\n");
}


void print(string_object* obj){
    printf("%s\n", obj->value);
}
