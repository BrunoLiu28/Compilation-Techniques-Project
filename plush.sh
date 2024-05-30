#!/bin/bash

# Function to print usage
usage() {
    echo "Usage: plush [--tree] filename.pl"
    exit 1
}

# Parse arguments
TREE_FLAG=0
FILE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --tree) TREE_FLAG=1 ;;
        *.pl) FILE="$1" ;;
        *) usage ;;
    esac
    shift
done

# Check if filename is provided
if [[ -z "$FILE" ]]; then
    usage
fi

# Main execution
if [[ $TREE_FLAG -eq 1 ]]; then
    python3 plush_compiler.py --tree "$FILE"
else
    python3 plush_compiler.py "$FILE"
fi
