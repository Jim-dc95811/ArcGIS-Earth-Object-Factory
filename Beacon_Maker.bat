@echo off
cd /d "%~dp0"
title EarthStick Beacon Maker 1.0
where py >nul 2>&1
if %errorlevel%==0 (
    py -3 Beacon_Maker.py
) else (
    python Beacon_Maker.py
)
pause
