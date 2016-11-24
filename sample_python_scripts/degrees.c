#include <mypyc.h>
#include <p_math.h>
float degrees_to_radians(float degrees)
{
  return p_math_module->radians(degrees);
}
float radians_to_degrees(float radians)
{
  return p_math_module->degrees(radians);
}
float fahrenheit_to_celsius(float fahrenheit)
{
  return (((fahrenheit) - (32)) * (5)) / (9);
}
float celsius_to_fahrenheit(float celsius)
{
  return (((9) * (celsius)) / (5)) + (32);
}
float celsius_to_kelvin(float celsius)
{
  return (celsius) + (273.15);
}
float kelvin_to_celsius(float kelvin)
{
  return (kelvin) - (273.15);
}
int main(int argc, char** argv)
{
  printf("%s %f\n", "180 deg to radians:", degrees_to_radians(180));
  printf("%s %f\n", "hardcoded 3.14159 to degrees:", radians_to_degrees(3.14159));
  printf("%s %f\n", "builtin math.pi to degrees:", radians_to_degrees(p_math_module->pi));
  printf("%s %f\n", "-40 deg fahrenheit to celsius:", fahrenheit_to_celsius(-(40)));
  printf("%s %f\n", "-459.67 deg fahrenheit to celsius:", fahrenheit_to_celsius(-(459.67)));
  printf("%s %f\n", "-40 deg celsius to fahrenheit:", celsius_to_fahrenheit(-(40)));
  printf("%s %f\n", "0 deg celsius to kelvin:", celsius_to_kelvin(0));
  printf("%s %f\n", "0 deg kelvin to celsius:", kelvin_to_celsius(0));
  return 0;
}