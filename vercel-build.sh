#!/bin/bash
echo "Starting custom build process..."

# Try to detect available Python versions
echo "Available Python versions:"
ls -la /usr/bin/python*
which python
python --version

# Force specific pip version
/usr/bin/python3.10 -m pip install --upgrade pip
/usr/bin/python3.10 -m pip install -r requirements.txt

echo "Build completed successfully"