#!/bin/bash

# check if python is installed
python3 -m venv quiz-venv
# check if venv already exists
source quiz-venv/bin/activate
pip3 install -r requirements.txt
clear
python3 main.py