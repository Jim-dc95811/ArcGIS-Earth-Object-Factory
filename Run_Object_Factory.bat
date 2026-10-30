@echo off
cd /d "%~dp0"
py -3 Object_Factory_v0.2_TEST.py
if errorlevel 1 python Object_Factory_v0.2_TEST.py
