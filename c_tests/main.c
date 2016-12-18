#include "mypyc.h"

int main(){
    mypyc_init();

    object_t* o = CALL(object);
    print(o);

    string_t* s = str_literal("test");
    print((object_t*)s);

    DECREF((object_t*)o);
    DECREF((object_t*)s);

    mypyc_terminate();
    return 0;
}
