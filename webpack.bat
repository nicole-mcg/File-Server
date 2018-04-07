@echo off
cd web
call "./node_modules/.bin/webpack" --watch
pause