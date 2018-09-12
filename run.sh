#!/bin/bash

pkill -f discordbot
source venv/bin/activate

cpath="$(realpath .)"
command="python3 $cpath/csbot/application.py &> $cpath/$(date -d "today" +"%Y%m%d%H%M".log) &"
bash -c "exec -a discordbot $command"
