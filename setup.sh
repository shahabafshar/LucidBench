#!/bin/bash

# Exit on error
set -e

# Install Python and pip if not present (assumes Ubuntu/Debian)
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Upgrade pip
python3 -m pip install --upgrade pip

# Install requirements
python3 -m pip install -r requirements.txt

# (Optional) Set up Jupyter kernel
python3 -m ipykernel install --user

echo "Setup complete." 