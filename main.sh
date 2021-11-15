#!/usr/bin/bash

# A small bash script for running all the necessary scripts/programs that are needed for this project. The purpose is to make this project easily reproducible.
# First we established a temp/ and an output/ folder if they have not existed. If temp existed before, delete all the contents inside that folder
# We create a virtualenv in order to be able to work with different dependencies so it will not interfere with other projects' dependencies.
# For being able to harness virtualenv, one needs to pip install it.
# Installing depencdencies via requirements.txt.
# Running 4 python scripts:
# 1.) First the NYT headline scrapers
# 2.) Reddit meme scrapers
# 3.) memes exploratory and label tagging ipynb
# 4.) a dataset splitter, that is a script that moves the picture in to their appropriate data set folders and generates 3 csv-s

rm -rf temp/*
mkdir temp/
mkdir output/

virtualenv temp/env -p python
. temp/env/bin/activate

pip install -r requirements.txt

python nyt_headline.py #> ./temp/logFile_headline.txt
python scrape_meme1118.py
python downl_meme1118.py
python meme_scrape.py
python meme_deletion.py
jupyter nbconvert --to notebook --execute memes_exploratory.ipynb --output memes_exploratory.ipynb
python splitting_dataset.py #>  ./temp/log.txt

deactivate

