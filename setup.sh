#!/bin/bash

# Check OS compatibility
if [ "$(lsb_release -d | awk '{print $2}')" != "Ubuntu" ]; then
    echo "This script is intended for Ubuntu LTS."
    exit 1
fi

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip llvm

# Additional setup steps
# ...

echo "Setup complete."
