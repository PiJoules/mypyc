#ifndef _BUILTIN_OBJS
#define _BUILTIN_OBJS


/**
 * Objects to be used
 */
typedef struct object_object object_object;
typedef struct string_object string_object;
typedef struct tuple_object tuple_object;
typedef struct dict_object dict_object;
typedef struct list_object list_object;


#define CLASS_PROPERTIES \
    tuple_object* parents;



/**
 * Object
 */

struct object_object {
    CLASS_PROPERTIES
    void (*__init__)(object_object* self);
    string_object* (*__str__)(object_object* self);
};

extern const object_object* const object;

object_object* new_object();


/**
 * String
 */

struct string_object {
    CLASS_PROPERTIES

    // Attrs
    char* value;
            
    // Methods
    void (*__init__)(string_object* self, char* str);
    string_object* (*__str__)(string_object* self);
};

extern const string_object* const string;

string_object* new_string(char* str);
string_object* empty_string();


/**
 * List
 */
//#define LIST_ATTRIBUTES \
//    OBJECT_ATTRIBUTES(list)
//
//struct list_object {
//    LIST_ATTRIBUTES
//};
//
//extern const list_object* const list;


/**
 * Tuple
 */

struct tuple_object {

};


///**
// * Dictionary
// */
//#define DICT_ATTRIBUTES \
//    OBJECT_ATTRIBUTES
//
//struct dict_object {
//    OBJECT_ATTRIBUTES
//};


#endif
