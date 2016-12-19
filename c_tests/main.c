#include "mypyc.h"
#include "fib.h"

int main(){
    mypyc_init();

    object_t* o = CALL(object);
    print(o);

    string_t* s = str_literal("test");
    print((object_t*)s);

    int_t* i = int_literal(123);
    print((object_t*)i);

    int_t* n = int_literal(40);
    int_t* fibn = CALL(fib, n);
    print((object_t*)fibn);

    DECREF((object_t*)fibn);
    DECREF((object_t*)n);
    DECREF((object_t*)i);
    DECREF((object_t*)s);
    DECREF((object_t*)o);

    mypyc_terminate();
    return 0;
}
