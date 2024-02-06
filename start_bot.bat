@REM This .bat script is for WINDOWS only. Python 3.9.x installed with py launcher enabled.
py -3.9 -m ensurepip --upgrade
py -3.9 -m pip install pip -U
py -3.9 -m pip install -r .\requirements.txt
py -3.9 bot.py
