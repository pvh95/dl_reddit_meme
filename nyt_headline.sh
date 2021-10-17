#!/usr/bin/bash
rm -rf temp/*
mkdir temp/
mkdir output/

virtualenv temp/env -p python
. temp/env/bin/activate

pip install -r requirements.txt

python nyt_headline.py > ./temp/logFile_headline.txt

deactivate

