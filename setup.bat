@echo off

echo This script will install Python and Node.js if they are not installed. It will do this with no interaction from you
echo.

echo [WARNING]
echo This will cause problems only if either is currently installed to a custom directory which is not on the system path
echo If this is the case, or you would like to install them yourself, please close this window now
echo.

echo This file can be rerun safely at any time to update pip requirements and node modules

pause

:: Run the powershell script
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process powershell -ArgumentList \"-NoProfile -ExecutionPolicy Bypass -File "%cd%/scripts/src/setup.ps1" -workingdirectory "%cd%"\" -Verb RunAs}"