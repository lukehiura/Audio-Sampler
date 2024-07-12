#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install uv
install_uv() {
    echo "Installing uv..."
    if command_exists curl; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command_exists wget; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "Error: Neither curl nor wget is installed. Please install one of them and try again."
        exit 1
    fi
    
    # Add uv to PATH for this session
    export PATH="$HOME/.cargo/bin:$PATH"
}

# Check if Homebrew is installed
if ! command_exists brew; then
    echo "Homebrew is not installed. Please install it from https://brew.sh/"
    exit 1
fi

# Install PortAudio
echo "Installing PortAudio..."
brew install portaudio

# Check if uv is installed, if not, install it
if ! command_exists uv; then
    install_uv
fi

# Create a virtual environment
echo "Creating virtual environment..."
uv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Set up environment for PortAudio
export LDFLAGS="-L/opt/homebrew/lib"
export CPPFLAGS="-I/opt/homebrew/include"

# Install setuptools first
echo "Installing setuptools..."
uv pip install setuptools

# Install the package in editable mode
echo "Installing audio_transcriber in editable mode..."
uv pip install -e .

echo "Setup complete. Virtual environment is activated."
echo "To start using the environment, run your Python script or type 'python' to open an interactive shell."
echo "When you're done, type 'deactivate' to exit the virtual environment."

# Offer to run the example script
if [ -f examples/simple_gui.py ]; then
    read -p "Do you want to run the example GUI script now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python examples/simple_gui.py
    fi
fi