@echo off
cd src
call python -m file_server.__init__ ../test_directories/client_dir localhost test test
pause