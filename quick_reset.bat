@echo off
cd scripts
echo Clearing test directories
call clear_test_dirs
echo Creating test files
call create_test_files
cd ..
call run_both