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


// void getArrayRandomFloats(float* m) {
//     printf("%f\n", m[1]);
// }

// float* getArrayRandomFloatsSize5(int size) {
//     // Seed the random number generator
//     srand(time(NULL));

//     // Allocate memory for an array of given size
//     float *arr = (float *)malloc(size * sizeof(float));
//     if (arr == NULL) {
//         printf("Memory allocation failed\n");
//         exit(1);
//     }

//     // Initialize the array with random numbers
//     for (int i = 0; i < size; i++) {
//         arr[i] = (float)rand() / RAND_MAX; // Generate random float between 0 and 1
//     }

//     return arr;
// }

float* getArrayRandomFloatsSize5() {
    // Allocate memory for an array of 5 integers
    float *arr = (float *)malloc(5 * sizeof(float));
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }

    // Initialize the array
    arr[0] = 9.7;
    arr[1] = 1.0;
    arr[2] = 3.3;
    arr[3] = 4.2;
    arr[4] = 5.1;

    return arr;
}

// float** createMatrix() {
//     // Allocate memory for the array of pointers to rows
//     float **matrix = (float **)malloc(4 * sizeof(float *));
//     if (matrix == NULL) {
//         printf("Memory allocation failed\n");
//         exit(1);
//     }

//     // Allocate memory for each row
//     for (int i = 0; i < 4; i++) {
//         matrix[i] = (float *)malloc(5 * sizeof(float));
//         if (matrix[i] == NULL) {
//             printf("Memory allocation failed\n");
//             exit(1);
//         }
//     }

//     // Initialize the matrix with some values
//     float value = 1.0;
//     for (int i = 0; i < 4; i++) {
//         for (int j = 0; j < 5; j++) {
//             matrix[i][j] = value;
//             value += 1.0;
//         }
//     }

//     return matrix;
// }

// int** createMatrix2() {
//     // Allocate memory for the array of pointers to rows
//     int **matrix = (int **)malloc(4 * sizeof(int *));
//     if (matrix == NULL) {
//         printf("Memory allocation failed\n");
//         exit(1);
//     }

//     // Allocate memory for each row
//     for (int i = 0; i < 4; i++) {
//         matrix[i] = (int *)malloc(5 * sizeof(int));
//         if (matrix[i] == NULL) {
//             printf("Memory allocation failed\n");
//             exit(1);
//         }
//     }

//     // Initialize the matrix with some values
//     int value = 1;
//     for (int i = 0; i < 4; i++) {
//         for (int j = 0; j < 5; j++) {
//             matrix[i][j] = value;
//             value += 1;
//         }
//     }

//     return matrix;
// }

int and(int a, int b) {
    return a && b;
}

int or(int a, int b) {
    return a || b;
}


// int float_array_length(float *array) {
//     printf("%ld\n", sizeof(array));
//     array = teste();
//     printf("%ld\n", sizeof(array));
//     printf("%ld\n", sizeof(float));
//     size_t size = sizeof(array) / sizeof(float);
//     printf("%ld\n", size);
//     return size;
// }