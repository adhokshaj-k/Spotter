#!/bin/bash

# Spotter Setup Script
# Automated installation and configuration

echo "========================================="
echo "  Spotter - Reconnaissance Framework"
echo "  Setup Script"
echo "========================================="
echo ""

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "[✗] Python is not installed"
    exit 1
fi

# Check Python version
echo "[*] Checking Python version..."
python_version=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [ "$major_version" -ge 3 ] && [ "$minor_version" -ge 8 ]; then
    echo "[✓] Python $python_version detected"
else
    echo "[✗] Python 3.8 or higher is required (found $python_version)"
    exit 1
fi

# Install Python dependencies
echo ""
echo "[*] Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "[✓] Python dependencies installed successfully"
else
    echo "[✗] Failed to install Python dependencies"
    exit 1
fi

# Check for nmap
echo ""
echo "[*] Checking for nmap..."
if command -v nmap &> /dev/null; then
    echo "[✓] nmap is installed"
else
    echo "[!] nmap is not installed (optional but recommended)"
    echo "    Install with: sudo apt-get install nmap"
fi

# Create results directory
echo ""
echo "[*] Creating results directory..."
mkdir -p results
echo "[✓] Results directory created"

# Make spotter.py executable
echo ""
echo "[*] Setting permissions..."
chmod +x spotter.py
echo "[✓] Permissions set"

# Test installation
echo ""
echo "[*] Testing installation..."
$PYTHON_CMD spotter.py --help > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "[✓] Installation successful!"
else
    echo "[✗] Installation test failed"
    exit 1
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Quick Start:"
echo "  $PYTHON_CMD spotter.py -t example.com --full"
echo ""
echo "For more information, see README.md"
echo ""
