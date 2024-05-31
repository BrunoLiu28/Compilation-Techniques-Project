#!/bin/bash

# Build the Docker image
docker build -t plush .

# Check if the operating system is Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Run the Docker container with interactive terminal using winpty
    winpty docker run -it plush:latest sh
else
    # Run the Docker container with interactive terminal
    docker run -it plush:latest sh
fi

echo "Done!"
