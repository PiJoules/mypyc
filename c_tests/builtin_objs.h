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

#define OBJ_NAME(name) name##_object

/**
 * Object
 */
#define OBJECT_ATTRIBUTES(name) \
    CLASS_PROPERTIES \
    void (*__init__)(OBJ_NAME(name)* self); \
    string_object* (*__str__)(OBJ_NAME(name)* self);

struct object_object {
    OBJECT_ATTRIBUTES(object)
};

extern const object_object* const object;

object_object* new_object(object_object* self);


/**
 * List
 */
#define STRING_ATTRIBUTES \
    OBJECT_ATTRIBUTES(string)

struct string_object {
    STRING_ATTRIBUTES
};

extern const string_object* const string;

object_object* new_object(object_object* self);


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
#define TUPLE_ATTRIBUTES \
    OBJECT_ATTRIBUTES

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
