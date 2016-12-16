#include "mypyc.h"

/**
 * Method declarations
 */
void __init__(string_object* self, char* str);
void __del__(string_object* self);
string_object* __str__(string_object* self);

/**
 * Attributes
 */
static class_properties props = {
};

/**
 * The actual object
 */
const string_object* const string = &(string_object){
    .props=props,

    .value=NULL,

    .__init__=__init__,
    .__del__=__del__,
    .__str__=__str__,
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
    self->value = (char*)malloc(strlen(str));
    strcpy(self->value, str);
}

void __del__(string_object* self){
    free(self->value);
    free(self);
}

string_object* __str__(string_object* self){
    return self;
}

