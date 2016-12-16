#include "mypyc.h"
#include "module.h"

int main(){
    string_object* s = new_string("test");
    del(s);

    return 0;
}
