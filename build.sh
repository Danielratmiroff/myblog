#!/bin/bash

OPEN="$1"

rm -rf site
python3 publish.py posts/*

if [ "$1" = "-o" ]; then
    explorer.exe .
fi
