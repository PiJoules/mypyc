#include "mypyc.h"

int main(){
    string_t* s = str_literal("test");
    print(s);
    DECREF((object_t*)s);

    return 0;
}
