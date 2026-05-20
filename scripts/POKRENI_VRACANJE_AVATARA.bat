@echo off
cd /d "%~dp0.."
py scripts\vrati_avatar_editor.py
if errorlevel 1 python scripts\vrati_avatar_editor.py
pause
