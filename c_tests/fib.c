#include "mypyc.h"
#include "fib.h"

static const fib_t fib_func;
static int_t* fib__exec__(int_t* n);

static const fib_t fib_func = {
    .__exec__=fib__exec__,
};

const fib_t* const fib = &fib_func;

static int_t* fib__exec__(int_t* n){
    if (n->value <= 0){
        return int_literal(0);
    }
    else if (n->value == 1){
        return int_literal(1);
    }
    else {
        int_t* n_m1 = int_literal(n->value - 1);
        int_t* n_m2 = int_literal(n->value - 2);
        int_t* fib_n_m1 = CALL(fib, n_m1);
        int_t* fib_n_m2 = CALL(fib, n_m2);
        int_t* sum = int_literal(fib_n_m1->value + fib_n_m2->value);

        DECREF((object_t*)fib_n_m2);
        DECREF((object_t*)fib_n_m1);
        DECREF((object_t*)n_m2);
        DECREF((object_t*)n_m1);

        return sum;
    }
}
