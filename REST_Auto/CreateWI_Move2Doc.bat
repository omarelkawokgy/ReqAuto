@echo off
:start
set PYTHON_PATH=C:\devTools\Python311\python.exe
set SCRIPT_PATH="%~dp0genParamScript.py"

%PYTHON_PATH% CreateWI_Move2Doc.py
pause
goto start
