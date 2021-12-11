# Dank or Not a.k.a predicting the popularity of Reddit memes


## Description 
The purpose of this project is to build Machine Learning / Deep Learning model(s) to be able to predict as accurately as possible whether a meme dank or not. The plan is to use cutting-edge ML/DL methods such as NLP for sentiment analysis and keyword extractions, and Convolutional Neural Networks (CNN) and Visual Transformers (ViT) for capture hidden patterns in meme pictures to achieve our above mentioned goal. 


## Data sources 
* Reddit's **memes** subreddit: https://www.reddit.com/r/memes/
* NYT Archives: https://www.nytimes.com/search/?srchst=nyt


## How to

### Install the project 

Prerequisities: 
* Python (3.7 or later)
* Jupyter Notebook/ JupyterLab for interactive ipynb session 
* 61GB or more storage 
* optional: Cloud or a PC with noticeable GPU power :) 
* **pip** package manager
* optional: install this convenience package: (targeted for Ubuntu 20.04LTS or later. This is important because in the main.sh all of the python scripts are called with pip/python. Without this package you have to run it with pip3 and python3) 
```
$ sudo apt install python-is-python3 
```
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
For more information about how scripts are deployed, consult the **main.sh** script.

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

**meme_scrape.py** 
  - A guide to create a Reddit API key: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
  - Scraping and downloading Reddit memes from 2019.01.01 until (but not including) 2021.10.17 and those pictures will be saved to **./output/meme_pics** folder
  - Any scraped text information (file_names, title, score) will be saved into the **./output/memes1921.csv**.

**scrape_meme1118.py**
   - It just scraped the necessary information and urls into a csv for another py script to download those memes via the url. 
   - Scraped period: 2011.01.01 - 2018.12.31
   - Saved to **./output/memes1118.csv**

**downl_meme1118.py**
   - Input: **./output/memes1118.csv**
   - It used the url information from **./output/memes1118.csv** to download memes to **./output/meme_pics/**
   - The # of downloaded images are much less than what this csv contains due to lot of already deleted memes from reddit. 
   
**meme_deletion.py**
   - Input: **./output/memes1118.csv** and **./output/memes1921.csv**
   - Concatenating  ./output/memes1921.csv and ./output/memes1118.csv into one dataframe then filter this dataframe by 
      - First using pics in ./faulty_pics folder to clean up ./output/meme_pics/
      - Then using the cleaned ./output/meme_pics/ folder to filter the concatenated dataframe
    
   - Output: **./output/memes.csv**

**memes_exploratory.ipynb** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pvh95/dl_reddit_meme/blob/main/memes_exploratory.ipynb)  (Exploratory Data Analysis and Visualization and labelling)  
  - Input: ***./output/memes.csv***
  - Output: ***./output/memes_prepared.csv***. It includes the label of each meme. 
  - Exploratory Data Analysis and Visualization and labelling 
  - Label our data whether it is dank or not. The method for this is using a sliding one-week window (where the meme in question is in the middle of this one-week window) to determine whether a meme are in the top 5%. If yes, we labelled it as dank (1), otherwise not (0).

**splitting_dataset.py** (Train-Valid-Test splitter)
   - Input: ***./output/memes_prepared.csv***
   - Output: ***./output/train_set.csv, ./output/valid_set.csv, ./output/test_set.csv***. Generating csv-s for the respecting datasets. 
   - Putting memes into their labelled **train_set/valid_set/test_set** subfolders inside the **./output** folders. For example a meme in the valid set and with a label 1, it will be put into **./output/valid_set/1/**.

**color_channel_conv.py** (converting RGBA/CMYK to RGB): 
   - Input: ***./output/train_set.csv, ./output/valid_set.csv, ./output/test_set.csv*** 
   - Output: ***./output/train_set.csv, ./output/valid_set.csv, ./output/test_set.csv***
   - Converting images with color channels other than RGB (such as CMYK, RGBA, P, L, LA) to RGB. (num of deviant pics were approximately 30.000) 
   - Furthermore, removing all the images whose pixel sizes (= width * height) are bigger than the PIL's limit pixel size, 89478485. (only 4 pics with this property were found and removed, all of them from ./output/train_set/0.)
   - Removing gif files as it cannot be converted to RGBA (for an obvious reason). 166 of them were removed. 
   - Removing hidden broken images detected by tf.io.decode_image (there were 3 or 4 of them).


### Train-Valid-Test Split 
The last 10.000 memes (in time order) are used for valid and test sets (which are approx. the last 3 months worth of memes). Accurately, these 10.000 memes are stratified sampled according to months with split ratio of 0.5. 

### Target 
In the ***./output/train_set.csv, ./output/valid_set.csv, ./output/test_set.csv***, the target variable is the **is_dank** binary variable. 0 = not dank, 1 = dank. The method of labelling a meme whether it is dank or not can be found above at the **memes_exploratory.ipynb** paragraph. 


## Results (so far)
At this point we managed to:
*  Scrape the last 10 years' of memes (from memes subreddit) with the daily cap of 200memes . (even though it is still not perfect, but try our best to adjust it as much as we could)
*  Deploy a better meme scraper for the earlier periods of the examined time interval.
*  Also scrape the last 10 years' New York Times headlines. This aspects enters into the picture when we try to harness the potential power of an actuality of a subject/topic. 
*  Do some initial explanatory data analysis and data visualization. 
*  Label our data whether it is dank or not. 
*  Do the train-valid-test split. With the help of our labelled data, we distributed those memes into the appropriate labelled train-valid-test folders a.k.a each of these three folders includes a '0' and '1' labelled folders. 

Numerically: 
* Memes are from 2011.10.02 until (but not including) 2021.10.17 (but no instances from 2013) a.k.a 10 years worth of memes with the max cap of 200 daily memes (in the earlier periods it was difficult to even scrape memes for a specific day) 
* test set: **4760** memes with label *0* and **240** memes with label *1* 
* valid set: **4741** memes with label *0* and **259** memes with label *1*
* train set: **235504** memes with label *0* and **12638** memes with label *1* 
* Total number of memes are: **258142**

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
* Harnessing the power of NLP for keyword extraction and sentiment analysis of memes (for the latter one, OCR could be deployed to get the texts from memes)
* Doing some feature extraction, data cleaning, data preprocessing 
* Implementing CNN and ViT models through Keras and PyTorch 
   - There will be baseline CNN models which is just gonna use only the memes, and no other information 
   - Multi-input Neural network model with one of the branch is CNN and the other branch is an MLP with already processed text data and other features. 
   - ViT for only images
   - Multi-input Neural network model with one of the branch will be ViT and the other will be a language module. 


## 2nd Milestone
* We purchased a Google Colab plan for better GPU.
* We uploaded the zipped folders to a shared Google Drive folder and these were loaded into the Colab environment.
* We made our base_model with RESNET. We removed the top layers and added appropriate layers for the classification task, also used pre-trained imagenet weigths.
* Wrapped into model_resnet, it has extra sequential and dense layers at the input and output parts.
   - Adam optimization was used, with binary_crossentropy and weighted accuracy metrics to account for class imbalance.
   - Early reduction and learning rate reducer were used for optimization.
   - Best model can be found in the same folder, we used checkpointer for that.
* Over 10 epoch, we plotted the training, validation accuracy, as well as cross entropy loss.
   - The training accuracy reaches around 0.61, validation accuracy 0.63.
   - The training loss reached 0.65, the validation loss 0.61.
* Evaluating on the test set, the loss ended at 0.58, the accuracy at 0.65.
* We extracted the true label from tf_dataset to get the probabilistic prediction and converted it into labels.
* We calculated the following metrics:
   - Accuracy: 0.6540
   - Precision: 0.0815
   - Recall: 0.6042
   - F1-score: 0.1436
   - Precision-Recall Curve AUC: 0.0913
   - ROC AUC: 0.6804
* We started fine-tuning.
   - We kept the first 400 layers frozen but trained the rest of them, using RMSPROP for 5 epochs.
* The validation accuracy climbed to 0.9 after 5 epochs, the cross entropy loss dropped to 0.5.
* Loss on the test was 0.46, accuracy 0.90.
* At this point, PR AUC was at 0.088 and ROC AUC at 0.664.
* We also used a model based on Xception for 15 epochs.
   - Its loss on the test set was 0.45, its accuracy 0.81.
   - The PR AUC equals 0.083, the ROC AUC at 0.622.
* Three "best models" were saved and exported to the folder, the resnet with and without fine tuning and the xcept model.


## About the authors 
- Bálint Turi-Kováts
- Pintér József
- Viet Hung Pham 


## Credits
We would like to pronounce our greatest thanks and gratitude to
- Roland Molontay (https://hsdslab.math.bme.hu/), 
- Péter Juhász (https://github.com/shepherd92)
- Beatrix Benkő (https://github.com/bbeatrix)

for their guidance and continuous help throughout the project process.
