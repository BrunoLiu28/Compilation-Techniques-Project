#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

//DEFAULT FUNCTIONS THAT COME WITH THE LANGUAGE
void print_int(int value) {
    printf("%d\n", value);
}

void print_float(float value) {
    printf("%f\n", value);
}

void print_bool(bool value) {
    printf("%s\n", value ? "true" : "false");
}

void print_char(char value) {
    printf("%c\n", value);
}

void print(const char* value) {
    printf("%s\n", value);
}

int pow_int (int base, int exp){
    int result = 1; // Initialize result to 1, as anything raised to the power of 0 is 1
    while (exp > 0) {
        result *= base; // Multiply result by base
        exp--; // Decrement exponent
    }
    return result;
}

float pow_float (float base, int exp){
    float result = 1; // Initialize result to 1, as anything raised to the power of 0 is 1
    while (exp > 0) {
        result *= base; // Multiply result by base
        exp--; // Decrement exponent
    }
    return result;
}

int and(int a, int b) {
    return a && b;
}

int or(int a, int b) {
    return a || b;
}

//USER FFI's

float* getArrayRandomFloatsSize5() {
    float *arr = (float *)malloc(5 * sizeof(float));
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }

    arr[0] = 9.7;
    arr[1] = 1.0;
    arr[2] = 3.3;
    arr[3] = 4.2;
    arr[4] = 5.1;

    return arr;
}


