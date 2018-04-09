@echo off
cd src
echo Testing back end
call python -m pytest
cd ..
pause