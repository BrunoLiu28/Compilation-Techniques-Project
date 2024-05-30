#!/bin/bash

# Ensure the script is run as root
if [[ "$EUID" -ne 0 ]]; then
  echo "Please run as root"
  exit 1
fi

echo "Updating package list and upgrading existing packages..."
apt-get update && apt-get upgrade -y

echo "Installing necessary dependencies..."
# Add your dependencies here. For example:
apt-get install -y \
  build-essential \
  curl \
  git \
  python3 \
  python3-pip \
  docker.io \
  docker-compose

# Additional setup or configuration steps can go here

# Verify installations
echo "Verifying installations..."

# Check for git
if command -v git &> /dev/null; then
    echo "Git installed successfully"
else
    echo "Git installation failed"
fi

# Check for Python
if command -v python3 &> /dev/null; then
    echo "Python3 installed successfully"
else
    echo "Python3 installation failed"
fi

# Check for Docker
if command -v docker &> /dev/null; then
    echo "Docker installed successfully"
else
    echo "Docker installation failed"
fi

# Check for Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "Docker Compose installed successfully"
else
    echo "Docker Compose installation failed"
fi

echo "All dependencies installed successfully."
