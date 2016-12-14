#include "mypyc.h"

string_object* __str__(object_object self);

static const list_object* const l = NULL;

const object_object* const object = &(object_object){
    l,
    __str__,
};
