#include <stdlib.h>
#include <stdio.h>

// Illegal
//enum e1 {
//    E1, E2
//};
//enum e2 {
//    E1, E2
//};


typedef struct obj1 obj1;
struct obj1 {
    void (*meth1)();
};


typedef struct obj2 obj2;
struct obj2 {
    void (*meth2)();
};


typedef enum ElemType ElemType;
enum ElemType {
    et_str,
    et_int,
    et_dbl,
};
typedef struct elem elem;
struct elem {
    ElemType type;
    union {
        char* str;
        int i;
        double d;
    };
};


typedef union mult_obj mult_obj;
union mult_obj {
    struct {
        int attr1;
    } ob1;
    struct {
        float attr1;
    } ob2;
};


void multi_print(elem* e){
    switch (e->type){
        case et_str:
            printf("%s\n", e->str);
            break;
        case et_int:
            printf("%d\n", e->i);
            break;
        case et_dbl:
            printf("%f\n", e->d);
            break;
    }
}


int main(){
    elem* arr = (elem*)malloc(sizeof(elem) * 3);
    arr[0].type = et_str;
    arr[0].str = "abc";


    printf("%s\n", arr[0].str);

    mult_obj a = {
        2,
    };

    printf("%d\n", a.ob1.attr1);


    elem e = {
        et_str,
        .str="somestr",
    };
    multi_print(&e);

    e = (elem){
        et_dbl,
        .d=3.14,
    };
    multi_print(&e);

    
    return 0;
}
