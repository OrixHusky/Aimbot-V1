@echo off
:: Request elevated (admin) privileges
powershell -Command "Start-Process -Verb RunAs python.exe aimbot.py"
