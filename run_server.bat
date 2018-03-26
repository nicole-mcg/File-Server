@echo off
cd src
call python -m file_server.file.__init__ ../test/serv_dir
pause