#!/bin/bash

echo "Installing pip requirements (Python must be installed)"
pip install -r requirements.txt

echo "Installing node modules (Node must be installed. Only required for building web)"
(cd web; npm install package.json)

echo "Creating test files"
(cd scripts; ./create_test_files.sh)

echo "Clearing test directories"
(cd scripts; ./clear_test_dirs.sh)