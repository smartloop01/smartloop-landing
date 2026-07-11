@echo off
cd /d "%~dp0"
flet run -w -d -r -p 8088 -a . main.py
pause
