#!/bin/bash
# Force Python 3.9
alias python=python3.9
alias pip=pip3.9
pip install --upgrade pip
pip install -r requirements.txt 

echo "Build completed successfully"