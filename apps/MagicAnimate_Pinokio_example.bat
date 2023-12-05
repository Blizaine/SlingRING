@echo off
SETLOCAL

:: Navigate to the script's base directory
cd C:\Users\bliza\pinokio\api\MagicAnimate.pinokio.git

:: Activate the virtual environment
CALL env\Scripts\activate.bat

:: Change to the app directory
cd app

:: Execute the Python command
python -m demo.gradio_animate

pause
