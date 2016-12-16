#include "mypyc.h"

/**
 * Method declarations
 */
static void __init__(string_object* self, char* str);
static void __del__(string_object* self);
static string_object* __str__(string_object* self);

/**
 * Attributes
 */
static class_properties _props = {
};

/**
 * The actual object
 */
string_object _string = {
    .props=NULL,

    .value=NULL,

    .__init__=__init__,
    .__del__=__del__,
    .__str__=__str__,
};
const string_object* const string = &_string;

string_object* new_string(char* str){
    string_object* new_str = (string_object*)malloc(sizeof(string_object));
    memcpy(new_str, string, sizeof(string_object));
    new_str->__init__(new_str, str);
    printf("created new str: %s\n", str);
    return new_str;
}

/**
 * Method definitions
 */

static void __init__(string_object* self, char* str){
    size_t len = strlen(str);
    self->value = (char*)malloc(len + 1);
    strncpy(self->value, str, len);
    self->value[len] = '\0';
    printf("string __init__\n");
    printf("str: %s\n", str);
    printf("val: %s\n", self->value);
}

static void __del__(string_object* self){
    free(self->value);
    printf("string del\n");
    free(self);
}

static string_object* __str__(string_object* self){
    return self;
}

