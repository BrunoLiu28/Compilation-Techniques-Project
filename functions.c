#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

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

void print_string(const char* value) {
    printf("%s\n", value);
}

void getArrayRandomFloats(int* m) {
    printf("%d\n", m[0]);
}

int* teste() {
    // Allocate memory for an array of 5 integers
    int *arr = (int *)malloc(5 * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }

    // Initialize the array
    arr[0] = 9;
    arr[1] = 2;
    arr[2] = 3;
    arr[3] = 4;
    arr[4] = 5;

    return arr;
}
