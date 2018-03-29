@echo off

echo Installing pip requirements (Python must be installed)
call pip install -r requirements.txt

echo Installing node modules (Node must be installed. Only required for building web)
cd web
call npm install package.json
cd ..


cd scripts

echo Creating test files
call create_test_files

echo Clearing test directories
call clear_test_dirs

cd ..