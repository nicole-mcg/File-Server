@echo off

cd scripts
echo Clearing test directories
call clear_test_dirs
echo Creating test files
call create_test_files
cd ..

start "Server" cmd /c run_server.bat
start "Client" cmd /c run_client.bat