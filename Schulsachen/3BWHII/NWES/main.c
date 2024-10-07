#include <stdio.h>
#include "embedded_code.h"

int add(int a, int b) {
    int ergebnis = a + b;
    return  ergebnis;
}

int main() {     
    int  a = 10;
    int  b = 20;
    float c = 1.123;
    float d = 4.5;
    float* p_c = &c;

    printf("c: %f, d: %f, p_c: %fon %x;  \n", c, d, p_c, p_c);

    c = 4.0f;
    printf("c: %f, d: %f, p_c: %fon %x;  \n", c, d,p_c, p_c);

    p_c = 5.0;
    printf("c: %f, d: %f, p_c: %fon %x;  \n", c, d,p_c, p_c);

    p_c = &d;
    printf("c: %f, d: %f, p_c: %fon %x;  \n", c, d, *p_c, p_c);


    int add_ergebnis = add(4,6);
    printf("Hallo Welt a: %i b: %i ergebnis: %i\n", a, b, add_ergebnis);
    printf("Hallo Welt c: %f on %x\n ", c, p_c);

    printf("Hallo Welt");


    return 0;
}
