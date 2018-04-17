@echo off

:: Run the powershell script
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process powershell -ArgumentList \"-NoProfile -ExecutionPolicy Bypass -File "%cd%/scripts/src/setup.ps1" -workingdirectory "%cd%"\" -Verb RunAs}"