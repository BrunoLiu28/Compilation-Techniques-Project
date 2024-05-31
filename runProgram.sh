#!/bin/bash

# Function to delete files if --rmaf flag is provided
function delete_files {
    rm -f llCode.s llCode.o functions.o a.out
}

function display_error {
    echo "Error: $1"
    exit 1
}

# Check if functions.c file exists
if [ ! -f "functions.c" ]
then
    display_error "The file 'functions.c' does not exist."
fi

# Run the LLVM compiler llc
llc llCode.ll || display_error "LLVM compilation failed."

# Compile the LLVM assembly into object files
gcc -c llCode.s || display_error "Compilation of 'llCode.s' failed."
gcc -c functions.c || display_error "Compilation of 'functions.c' failed."

# Link the object files and generate the executable
gcc -no-pie -fno-PIE llCode.o functions.o -o a.out || display_error "Linking failed."

# Run the executable
./a.out || display_error "Execution of 'a.out' failed."

# Check if the --rmaf flag is provided
if [[ "$1" == "--rmaf" ]]; then
    # Delete the originated files
    delete_files || display_error "Deletion of files failed."
fi
