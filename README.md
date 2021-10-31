# Dank or Not a.k.a predicting the popularity of Reddit memes


## Description 
The purpose of this project is to build Machine Learning / Deep Learning model(s) to be able to predict as accurately as possible whether a meme dank or not. The plan is to use cutting-edge ML/DL methods such as NLP for sentiment analysis and keyword extractions, and Convolutional Neural Networks (CNN) and Visual Transformers (ViT) for capture hidden patterns in meme pictures to achieve our above mentioned goals. The reason for turning to ML/DL instead of "carrying out Software1 solution" is that there are lot of hidden patterns in the data that would be difficult to recognize with the good old method. Furthermore, with the conventional method, it would make it highly difficult to set rules for any potential patterns that might crop up. 



## Data sources 
* Reddit's **memes** subreddit: https://www.reddit.com/r/memes/
* NYT Archives: https://www.nytimes.com/search/?srchst=nyt


## How to

### Install the project 

Prerequisities: 
* Python (3.7 or later)
* Jupyter Notebook/ JupyterLab for interactive ipynb session 
* 50GB of storage 
* optinal: Cloud or a PC with noticeable GPU power :) 
* **pip** package manager
* optional: **virtualenv** (for seperating this project dependencies from others and also great for reproducibility), **CL** (unix/linux CL is the preferable one) 

### Install the necessary dependencies/packages (so far): 
* https://github.com/pvh95/dl_reddit_meme/blob/main/requirements.txt
* Can install them one-by-one
```
$ pip install <package_name>==<package_version>
```
* Using the following to one-liner would do the trick 
```
$ pip install -r requirements.txt
```

### Use the project
Setting up the dev 
* Either fork the project or
* Clone the repository 
```
$ git clone https://github.com/pvh95/dl_reddit_meme.git <target_folder_on_your_computer>
```

### Structure the project: 
* **'./'** the root directory. Most of the scripts will be here. 
* Inside the root directory, there are two main subdirectories. First, **./temp** which is supposed to be used for anything temporary (e.x. logging files there for example or activating the virtualenv). The other one is the **./output** folder where the results of scripts will be dumped.

If you are coming from a Unix/Linux based computer, you just need to type the following one-liner into the CL:
```
$ sh main.sh
```
It will install all the dependencies, create the virtual environment and run the scripts/programs that will be discussed in details in the next section.


## Methods 

### Scripts used in the project
These script are placed in the **./** root folders.

**requirements.txt**: list all the dependencies that our programs/scripts need.

**main.sh**: The activator of running all the programs/scripts.

**nyt_headline.py** (NYT headline scraping): 
  - Need to create an NYT API here: https://developer.nytimes.com/docs/archive-product/1/overview (further instruction can be read on the website)
  - the monthly headline csv-s will be saved to the **./output/headlines** folder
  - Output: the encompassing **./output/unified_headline.csv**
  - It includes the last 10 years of scraped headlines with addtional information such *date*, *section*, *keywords*

**meme_scrape.py** (Reddit Meme scraper)
  - A guide to create a Reddit API key: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
  - Scraping Reddit memes from 2011.10.02 until (but not including) 2021.10.17 and those pictures will be saved to **./output/meme_pics** folder
  - Any text information (file_names, title, score) will be saved into the **./output/memes.csv**.

**memes_exploratory.ipynb** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pvh95/dl_reddit_meme/blob/main/memes_exploratory.ipynb)  (Exploratory Data Analysis and Visualization and labelling)  
  - Input: ***./output/memes.csv***
  - Output: ***./output/memes_prepared.csv***. It includes the label of each meme. 
  - Exploratory Data Analysis and Visualization and labelling 
  - Label our data whether it is dank or not. The method for this is using a sliding one-week window (where the meme in question is in the middle of this one-week window) to determine whether a meme are in the top 5%. If yes, we labelled it as dank (1), otherwise not (0).

**splitting_dataset.py** (Train-Valid-Test splitter)
   - Input: ***./output/memes_prepared.csv***
   - Output: ***./output/train_set.csv, ./output/valid_set.csv, ./output/test_set.csv***. Generating csv-s for the respecting datasets. 
   - Putting memes into their labelled **train_set/valid_set/test_set** subfolders inside the **./output** folders. For example a meme in the valid set and with a label 1, it will be put into **./output/valid_set/1/**.

### Train-Valid-Test Split 
The last 10.000 memes (in time order) are used for valid and test sets (which are approx. the last 3 months worth of memes). Accurately, these 10.000 memes are stratified sampled according to months with split ratio of 0.5. 

### Target 
In the ***./output/train_set.csv, ./output/valid_set.csv, ./output/test_set.csv***, the target variable is the **is_dank** binary variable. 0 = not dank, 1 = dank. The method of labelling a meme whether it is dank or not can be found above at the **memes_exploratory.ipynb** paragraph. 


## Results (so far)
At this point we managed to:
*  Scrape the last 10 years' of memes (from memes subreddit) with the daily cap of 200-250 memes. (even though it is still not perfect, but try our best to adjust it as much as we could)
*  Also scrape the last 10 years' New York Times headlines. This aspects enters into the picture when we try to harness the potential power of an actuality of a subject/topic. 
*  Do some initial explanatory data analysis and data visualization. 
*  Label our data whether it is dank or not. 
*  Do the train-valid-test split. With the help of our labelled data, we distributed those memes into the appropriate labelled train-valid-test folders a.k.a each of these three folders includes a '0' and '1' labelled folders. 

Numerically: 
* Memes are from 2011.10.02 until (but not including) 2021.10.17 (but no instances from 2013) a.k.a 10 years worth of memes with the max cap of 200-250 memes
* test set: **4759** memes with label *0* and **241** memes with label *1* 
* valid set: **4735** memes with label *0* and **265** memes with label *1*
* train set: **155105** memes with label *0* and **8340** memes with label *1* 

Main data: 
* labelled dataset representing csv-s are: 
   - ./output/train_set.csv, 
   - ./output/valid_set.csv, 
   - ./output/test_set.csv
* headline csv-s: **./output/unified_headlines.csv**
* folders where memes are placed according to the 3 labelled datasets representing csv-s: (they are gitignored)
    - ./output/train_set/0/
    - ./output/train_set/1/
    - ./output/valid_set/0/
    - ./output/valid_set/1
    - ./output/test_set/0
    - ./output/test_set/1


## Plan 
* Deploying a better meme scraper
* Doing further data analysis and visualization. 
* Using **shap** values to determine how features might influence the prediction.
* Harnessing the power of NLP for keyword extraction and sentiment analysis of memes (for the latter one, OCR could be deployed to get the texts from memes)
* Doing some feature extraction, data cleaning, data preprocessing 
* Implementing CNN and ViT models through Keras and PyTorch 


## About the authors 
- Bálint Turi-Kováts
- Pintér József
- Viet Hung Pham 


## Credits
We would like to pronounce our greatest thanks and gratitude to
- Roland Molontay (https://hsdslab.math.bme.hu/), 
- Péter Juhász (https://github.com/shepherd92)

for their guidance and continuous help throughout the project process.
