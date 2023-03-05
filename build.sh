#!/bin/bash

# venv
pip install venv
python3 -m venv voiceChat
source ./voiceChat/Scripts/activate

# install requirements
pip install -r requirements.txt

# make a build
pip install pyinstaller
pyinstaller main.spec


