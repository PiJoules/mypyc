#ifndef _BUILTIN_OBJS
#define _BUILTIN_OBJS


/**
 * Objects to be used
 */
typedef struct object_t object_t;
typedef struct string_t string_t;
//typedef struct tuple_object tuple_object;
//typedef struct dict_object dict_object;
//typedef struct list_object list_object;

typedef struct class_properties class_properties;

struct class_properties {
};


/**
 * Object
 */

struct object_t {
    class_properties* props;

    // Props
    size_t ref_count;

    // Methods
    //void (*__init__)(object_t* self);
    //void (*__del__)(object_t* self);
    //string_t* (*__str__)(object_t* self);
    object_t* (*__exec__)();
    object_t* __init__;
    object_t* __del__;
    object_t* __str__;
};

object_t* object();


/**
 * String
 */

struct string_t {
    class_properties* props;

    // Object props
    size_t ref_count;

    // Methods
    void (*__init__)(string_t* self, char* str);
    void (*__del__)(string_t* self);
    string_t* (*__str__)(string_t* self);

    // String attrs
    char* value;
};

string_t* str_literal(char* str);

struct str_kwargs {
    object_t* object;
    object_t* encoding;
    object_t* errors;
};
string_t* str(struct str_kwargs kwargs);
string_t* str_base(object_t* object, object_t* encoding, object_t* errors);

string_t* empty_string();


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
