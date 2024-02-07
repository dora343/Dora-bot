#!/bin/bash
git update-index --skip-worktree settings.json
git update-index --skip-worktree cmds/minigame-data.json
python3 ensurepip --upgrade
pip install pip --upgrade
pip install -r requirements.txt
python3 bot.py