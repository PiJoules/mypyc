#include "mypyc.h"

/**
 * Method declarations
 */
void __init__(string_object* self, char* str);
string_object* __str__(string_object* self);

/**
 * Attributes
 */
tuple_object l;

/**
 * The actual object
 */
const string_object* const string = &(string_object){
    &l,
    NULL,
    __init__,
    __str__,
};

string_object* new_string(char* str){
    string_object* new_str = (string_object*)malloc(sizeof(string_object));
    memcpy(new_str, string, sizeof(string_object));
    new_str->__init__(new_str, str);
    return new_str;
}

/**
 * Method definitions
 */

void __init__(string_object* self, char* str){
}

string_object* __str__(string_object* self){
    return NULL;
}

