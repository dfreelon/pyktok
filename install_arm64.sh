#!/bin/bash

# ARM64 Installation Script for pyktok
# This script installs pyktok with ARM64-compatible dependencies

echo "Installing pyktok for ARM64 (Raspberry Pi)..."

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    chromium-browser \
    chromium-chromedriver \
    wget \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv pyktok_arm64_env
source pyktok_arm64_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install ARM64-compatible dependencies
echo "Installing ARM64-compatible Python packages..."
pip install --no-binary :all: \
    beautifulsoup4 \
    browser-cookie3 \
    numpy \
    pandas \
    requests \
    streamlit \
    selenium \
    webdriver-manager

# Install pyktok ARM64 version
echo "Installing pyktok ARM64 version..."
pip install -e .

echo "Installation complete!"
echo ""
echo "To use pyktok on ARM64:"
echo "1. Activate the virtual environment: source pyktok_arm64_env/bin/activate"
echo "2. Import the ARM64 version: from pyktok import pyktok_arm64 as pyktok"
echo "3. Specify browser: pyktok.specify_browser('chrome')"
echo ""
echo "Note: Make sure Chrome/Chromium is installed and accessible"
