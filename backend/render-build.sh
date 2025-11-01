#!/bin/bash
# Install potrace from source since we don't have sudo access
set -e

echo "Installing potrace..."

# Download and compile potrace
cd /tmp
wget http://potrace.sourceforge.net/download/1.16/potrace-1.16.linux-x86_64.tar.gz
tar -xzf potrace-1.16.linux-x86_64.tar.gz
cp potrace-1.16.linux-x86_64/potrace /opt/render/project/src/backend/

# Go back to project directory
cd /opt/render/project/src/backend

# Install Python dependencies
pip install -r requirements.txt

echo "Build complete!"
