import pandas as pd 
import os
import numpy as np

from PIL import Image
from os import listdir
from os.path import isfile, join


col_names=['id', 'title', 'text', 'score']
memes1921 = pd.read_csv('./output/memes1921.csv', sep=';', names=col_names, header=None) 
memes1118 = pd.read_csv('./output/memes1118.csv')

memes1118.drop(columns = ['text', 'num_comments', 'url'], inplace = True)
memes1921.drop(columns = ['text'], inplace = True)
memes = pd.concat([memes1118, memes1921], ignore_index = True)
memes = memes.dropna(subset=['score']).reset_index(drop = True) #Throwing out instances where score value is NA -- only 8 cases like this
memes['score'] = memes['score'].astype('int32')

onlyfiles = [f for f in listdir('./output/meme_pics/') if isfile(join('./output/meme_pics/', f))]

faulty1 = Image.open('./faulty_pic/faulty1.jpg')
faulty2 = Image.open('./faulty_pic/faulty2.png')

for pic in onlyfiles:
    try:
        img_temp=Image.open('./output/meme_pics/' + pic)
        s1=np.array(img_temp)==np.array(faulty1)
        s2=np.array(img_temp)==np.array(faulty2)
        if type(s1)==bool and type(s2)==bool:
            continue
        elif s1.all()==True:
            os.remove('./output/meme_pics/' + pic)
        elif s2.all()==True:
            os.remove('./output/meme_pics/'+pic)
    except:
        os.remove('./output/meme_pics/' + pic)


onlyfiles = [f for f in listdir('./output/meme_pics/') if isfile(join('./output/meme_pics/', f))]
d = {'fname': onlyfiles}
df = pd.DataFrame(data=d)

scraped_df = df['fname'].str.rsplit('.', n = 1, expand = True)
df['id'] = scraped_df[0]

memes_trial = memes.merge(df, on='id')
memes_trial.to_csv('./output/memes.csv', index = False)



