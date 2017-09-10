#!/bin/bash
cd /home/dinnerBot
source venv/bin/activate
. ./config.sh
python main.py 
deactivate
