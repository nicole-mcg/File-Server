@echo off
cd src
call python -m file_server.file.__init__ ../test_directories/serv_dir
pause