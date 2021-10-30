#!/usr/bin/bash
rm -rf temp/*
mkdir temp/
mkdir output/

virtualenv temp/env -p python
. temp/env/bin/activate

pip install -r requirements.txt

python nyt_headline.py > ./temp/logFile_headline.txt
python meme_scrape.py
jupyter nbconvert --to notebook --execute memes_exploratory.ipynb --output memes_exploratory.ipynb
python splitting_dataset.py >  ./temp/log.txt

deactivate

