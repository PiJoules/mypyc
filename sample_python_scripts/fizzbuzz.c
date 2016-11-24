#include <mypyc.h>
void fizzbuzz(int n)
{
  for (int i = 1; i < (n) + (1); i += 1)
  {
    if ((!((i) % (3))) && (!((i) % (5))))
    {
      printf("%s\n", "fizzbuzz");
    }
    else
      if (!((i) % (3)))
      {
        printf("%s\n", "fizz");
      }
      else
        if (!((i) % (5)))
        {
          printf("%s\n", "buzz");
        }
        else
        {
          printf("%d\n", i);
        }
  }
}
int main(int argc, char** argv)
{
  fizzbuzz(15);
  return 0;
}