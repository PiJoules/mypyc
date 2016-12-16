#include "mypyc.h"
#include "module.h"

int main(){
    string_object* s = new_string("test");
    print(s);
    del(s);
    printf("sizeof string_object: %zu\n", sizeof(string_object));
    printf("sizeof string __init__: %zu\n", sizeof(string->__init__));

    return 0;
}
