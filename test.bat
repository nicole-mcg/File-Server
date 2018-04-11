@echo off

cd src
echo Testing back end
call python -m pytest
cd ..

cd web
echo Testing front end
call npm test
cd ..

cd scripts
echo Cleaning up test files
call cleanup_tests
cd ..

pause