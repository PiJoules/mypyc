#include "mypyc.h"


void del(object_t* obj){
    CALL(obj->__del__, obj);
}


void print(string_t* obj){
    printf("%s\n", obj->value);
}
