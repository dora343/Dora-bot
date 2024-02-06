#!/bin/bash

python ensurepip --upgrade
pip install pip --upgrade
pip install -r requirements.txt
python3 bot.py