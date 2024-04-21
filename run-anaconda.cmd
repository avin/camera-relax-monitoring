@echo off
set CONDA_PATH=%USERPROFILE%\anaconda3

set CONDA_ENV=base

call "%CONDA_PATH%\Scripts\activate.bat" %CONDA_ENV%

python ./main.py
