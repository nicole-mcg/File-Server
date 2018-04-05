#!/bin/bash

echo "Installing pip requirements (Python must be installed)"
pip install -r requirements.txt

echo "Installing node modules (Node must be installed. Only required for building web)"
cd web
npm install package.json
cd ..

cd scripts

echo "Creating test files"
./create_test_files.sh

echo "Clearing test directories"
./clear_test_dirs.sh

cd ..