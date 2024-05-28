#include <stdio.h>
#include <stdbool.h>

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

int getArrayRandomFloats() {
    return 4;
}
