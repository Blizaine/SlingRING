@echo off

REM Create the virtual environment
python -m venv myenv

REM Activate the virtual environment
call myenv\Scripts\activate.bat

REM Install the required packages
pip install gradio==3.50.2
pip install os
pip install subprocess
pip install psutil
pip install logging
pip install gputil



pause