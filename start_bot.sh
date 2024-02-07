#!/bin/bash
git update-index --skip-worktree settings.json
git update-index --skip-worktree cmds/minigame-data.json
# python3 ensurepip --upgrade
python3 -m venv venv
source venv/bin/activate

pip install pip --upgrade
pip install -r requirements.txt
python3 bot.py
source venv/bin/deactivate