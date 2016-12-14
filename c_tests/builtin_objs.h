#ifndef _BUILTIN_OBJS
#define _BUILTIN_OBJS


/**
 * Objects to be used
 */
typedef struct object_object object_object;
typedef struct string_object string_object;
typedef struct list_object list_object;


#define CLASS_PROPERTIES \
    list_object* parents;

/**
 * Object
 */
#define OBJECT_ATTRIBUTES \
    CLASS_PROPERTIES \
    string_object* (*__str__)(object_object self);

struct object_object {
    OBJECT_ATTRIBUTES
};

extern const object_object* const object;


/**
 * List
 */
#define STRING_ATTRIBUTES \
    OBJECT_ATTRIBUTES

struct string_object {
    STRING_ATTRIBUTES
};

extern const string_object* const string;


/**
 * List
 */
#define LIST_ATTRIBUTES \
    OBJECT_ATTRIBUTES

struct list_object {
    LIST_ATTRIBUTES
};

extern const list_object* const list;


#endif
