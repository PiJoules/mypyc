#include "mypyc.h"
#include "module.h"

struct S {
    int i;
    char c;
    float f;
};

int main(){
    struct S* s = &(struct S){
        10,
        'A'
    };

    printf("%c %zu %zu %zu\n", module->c, sizeof(struct S), sizeof(*s), sizeof(struct S*));
    return 0;
}
