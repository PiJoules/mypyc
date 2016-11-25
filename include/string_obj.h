#ifndef _STRING_OBJ_H
#define _STRING_OBJ_H

// TODO: Just make wrapper functions for char arrays for now.
typedef struct string string;
struct string {
    char* buffer;
    int length;

    // Functions
    string (*replace)(string old, string new);
};

#endif
