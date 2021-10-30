# Dank or Not a.k.a predicting the popularity of Reddit memes

## Description 
The purpose of this project is to build Machine Learning / Deep Learning model(s) to be able to predict whether a meme dank or not. The plan is to use cutting-edge ML/DL methods such as Convolutional Neural Networks (CNN) and Visual Transformers (ViT) to achieve our goals. 

At this point we managed to:
*  Scrape the last 10 years' of memes (from memes subreddit) with the daily cap of 200-250 memes. (even though it is still not perfect, but try our best to adjust it as much as we could)
*  Also Scrape the last 10 years' New York Times headlines. This aspects enters into the picture when we try to harness the potential power of an actuality of a subject/topic. 
*  Do some initial explanatory data analysis and data visualization. 
*  Label our data whether it is dank or not. The method for this it using a sliding one-week window (where the meme in question is in the middle of this one-week window) to determine whether a meme are in the top 5%. If yes, we labelled it as dank (1), otherwise not (0).
*  Do the train-valid-test split. With the help of our labelled data, we distributed those memes into the appropriate labelled train-valid-test folders a.k.a each of these three folders includes a '0' and '1' labelled folders. 

Plan for the rest of the course: 
* Egeszitsetek ki mar pls bmi relevanssal, en mar agyhalott vagyok este 12:30-kor :')
* Deploy a better meme scraper
* Do further data analysis and visualization. 
* Using shap values to determine how features might influence the prdiction.
* Do some feature extraction, data cleaning, data preprocessing 
* Implementing CNN and ViT models through Keras and PyTorch 

## How to install the project: 
What one might needs: 
* Python (3.7 or later)
* Jupyter Notebook 
* Clolud or a PC with a noticeable GPU power :) 
* **pip** package manager
* optional: **virtualenv** (for seperating this project depencdencies from others and also great for reproducibility), **CL** (unix/linux CL is the preferable one) 

Necessary dependencies/packages (so far): 
* https://github.com/pvh95/dl_reddit_meme/blob/main/requirements.txt
* Can install them one-by-one
```
pip install <packagename>
```
* Using the following to one-liner would do the trick 
```
pip install -r requirements.txt
```
## How to use the projects
Structure of this projects: 
* **'./'** the root directory. Most of the scripts will be here. 
* Inside the root directory, two main subdirectory. First, **./temp** which is supposed to use for anything temporary. (logging files there for example). The other one is the **./output** folder where the results of scripts will be dumped here.

First clone or fork this project. If you are coming from a Unix/Linux based computer, you are a lucky duck, you just need to type the following into the CL:
```
sh main.sh
```
It will install all the dependencies, create the virtual environment and run the scripts/programs that will be discussed in details in the next paragraph

## Code components of this project

**requirements.txt**: list all the dependencies that our programs/scripts need.

**main.sh**: The activator of running all the programs/scripts.

**nyt_headline.py** (NYT headline scraping): 
  - the monthly headline csv-s will be saved to the ./output/headlines folder
  - the encompassing unified_headline.csv will be saved to the ./output folder
  - It includes the last 10 years of scraped 

**meme_scrape.py** (Reddit Meme scraper)
  - Scraping Reddit memes from 2011.10.02 until (but not including) 2021.10.17 and those pictures will be saved to **./output/meme_pics** folder
  - Any text information (file_names, corresponding text, score) will be saved into the memes.csv in the **./output** folder.

**memes_exploratory.ipynb** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pvh95/dl_reddit_meme/blob/main/memes_exploratory.ipynb)  (Exploratory Data Analysis and Visualization and labelling) 
  - Balint ird mar meg itt mit csinaltal pls
  - Output: memes_prepared.csv in the **./output** folder.

**splitting_dataset.py** (Train-Valid-Test splitter)
   - Generating csv-s for the respecting dataset. Output train_set.csv, valid_set.csv, test_set.csv int the **./output** folders
   - Putting memes into the labelled train_set, valid_set, test_set inside the **./output** folders.

## Credits
Roland Molontay, Péter Juhász

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pvh95/dl_reddit_meme/blob/main/memes_exploratory.ipynb)
