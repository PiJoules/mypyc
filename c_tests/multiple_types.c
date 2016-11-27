#include <mypyc.h>
typedef enum ElemType_mult_type_ic1 ElemType_mult_type_ic1;
enum ElemType_mult_type_ic1 {
        mult_type_ic1_int_0,
    mult_type_ic1_char_1,

};
typedef struct mult_type_ic1 mult_type_ic1;
struct mult_type_ic1 {
        ElemType_mult_type_ic1 type;
    union  {
        int t0;
    char* t1;

};


};

void multi_print(mult_type_ic1 x){
    switch (x.type){
        case mult_type_ic1_int_0:
            printf("%d\n", x.t0);
            break;
        case mult_type_ic1_char_1:
            printf("%s\n", x.t1);
            break;
    }
}

int main()
{
  //mult_type_ic1 x = 2;
  //printf("%d\n", x);
  //x = "a";
  //printf("%s\n", x);

  mult_type_ic1 x = (mult_type_ic1){
      mult_type_ic1_int_0,
      .t0=2,
  };
  multi_print(x);
  x = (mult_type_ic1){
      mult_type_ic1_char_1,
      .t1="abc",
  };
  multi_print(x);


  return 0;
}
