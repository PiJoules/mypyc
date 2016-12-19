#ifndef _FIB_H
#define _FIB_H

typedef struct fib_t fib_t;
struct fib_t {
    int_t* (*__exec__)(int_t* n);

    class_properties* props;

    // Props
    size_t ref_count;
};

extern const fib_t* const fib;


#endif
