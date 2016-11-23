#include <mypyc.h>
#include <p_math.h>


float p_math_radians(float);
float p_math_degrees(float);


static const p_math __p_math_module = {
    M_PI,
    p_math_radians,
    p_math_degrees,
};
const p_math* p_math_module = &__p_math_module;


float p_math_radians(float degrees){
    return degrees * M_PI / 180.0;
}

float p_math_degrees(float radians){
    return radians * 180.0 / M_PI;
}



