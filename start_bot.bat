@REM This .bat script is for WINDOWS only. Python 3.9.x installed with py launcher enabled.

py -3.9 -m venv venv
call "venv\Scripts\activate.bat"

python -m pip install pip -U
python -m pip install -r .\requirements.txt
python bot.py
call "venv\Scripts\deactivate.bat"