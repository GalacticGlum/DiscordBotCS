#!/bin/bash

python3 csbot/application.py > $(date -d "today" +"%Y%m%d%H%M").log &
