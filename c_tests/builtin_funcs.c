#include "mypyc.h"

void mypyc_init(){
    str_default_kwarg_object = (object_t*)str_literal("");
    str_default_kwarg_encoding = str_literal("utf-8");
    str_default_kwarg_errors = str_literal("strict");
}

void mypyc_terminate(){
    del((object_t*)str_default_kwarg_object);
    del((object_t*)str_default_kwarg_encoding);
    del((object_t*)str_default_kwarg_errors);
}


void del(object_t* obj){
    CALL(obj->__del__, obj);
    free(obj);
}


void print(object_t* obj){
    string_t* tmp_obj_str = CALL(str, obj, (string_t*)str_default_kwarg_encoding, (string_t*)str_default_kwarg_encoding);
    printf("%s\n", tmp_obj_str->value);
    DECREF(tmp_obj_str);
}
