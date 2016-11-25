#ifndef _P_MATH_H
#define _P_MATH_H

typedef struct p_math p_math;
struct p_math {
    // Constants
    float pi;

    // Functions
    float (*radians)(float degrees);
    float (*degrees)(float radians);
};


extern const p_math* p_math_module;


#endif
