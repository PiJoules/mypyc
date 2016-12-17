#include "mypyc.h"
#include "module.h"


typedef struct kwargs kwargs;
struct kwargs {
    int arg1;
    int arg2;
};

#define test(...) test_unpack((kwargs){.arg1=1, .arg2=2, __VA_ARGS__})
void test_base(int arg1, int arg2){
    printf("%d %d\n", arg1, arg2);
}
void test_unpack(kwargs args){
    test_base(args.arg1, args.arg2);
}


int func(){
    srand(time(NULL));
    return rand();
}


int main(){
    string_object* s = new_string("test");
    print(s);
    del(s);
    printf("sizeof string_object: %zu\n", sizeof(string_object));
    printf("sizeof string __init__: %zu\n", sizeof(string->__init__));

    test(.arg2=func());

    return 0;
}
