#ifndef _OBJECT_H
#define _OBJECT_H

#include "string_obj.h"


typedef struct object object;
struct object {
    
    string* (*__str__)(object self);
};

#endif
