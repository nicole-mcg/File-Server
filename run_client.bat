@echo off
call python -m file_server.file.__init__ ./test/client_dir localhost
pause