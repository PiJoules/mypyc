#ifndef _BUILTIN_OBJS
#define _BUILTIN_OBJS


/**
 * Objects to be used
 */
typedef struct object_t object_t;
typedef struct string_t string_t;
typedef struct int_t int_t;
//typedef struct tuple_object tuple_object;
//typedef struct dict_object dict_object;
//typedef struct list_object list_object;

typedef struct class_properties class_properties;

struct class_properties {
};


#define METHOD_WRAPPER_ATTRS \
    class_properties* props; \
    size_t ref_count; \
    object_t* __init__; \
    object_t* __del__; \
    object_t* __str__; \
    object_t* __int__;


/**
 * Object
 */
#include "object.h"


/**
 * String
 */
#include "string_obj.h"


#include "int_obj.h"


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

//struct tuple_object {
//
//};
//
//extern const tuple_object* const tuple;
//
//tuple_object* new_tuple(int, ...);


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
