from PIL import Image
import os
from os import listdir
from os.path import isfile, join

import pandas as pd 
import numpy as np 


output_set = './output/'
dirname = ['train_set', 'valid_set', 'test_set']
subdirname = ['0', '1']
#Creating 6 path to 6 folders which comprise of train/valid/test main folder and each of them has 0 or 1 as subfolders 
fullpath_sets = [str(join(output_set, dirn, subdirn + '/')) for dirn in dirname for subdirn in subdirname] 

train_df = pd.read_csv(output_set + 'train_set.csv')
valid_df = pd.read_csv(output_set + 'valid_set.csv')
test_df = pd.read_csv(output_set + 'test_set.csv')


for fps in fullpath_sets:
    onlyfiles = [f for f in listdir(fps) if isfile(join(fps, f))]  #Listing all the files in one of the 6 folders 
    
    fourChannel_lst = list()   # Creating a list for all the files whose color channels are either RGBA or CMYK 
    explode_lst = list()    #Creating a list for all the files whose pixels (= width * height) are too big 
    
    for pic in onlyfiles:
        try:
            img = Image.open(fps + pic)
            if img.size[0] * img.size[1] > 89478485:   # Removing all the images whose pixel sizes are bigger than the PIL's limit pixel size
                explode_lst.append(pic)  
                os.remove(fps + pic)
                continue

            else:
                num_bands = len(img.getbands())
                if num_bands == 4: #If color channels are 4 (RGBA, CMYK)
                    fourChannel_lst.append(pic)

        except: 
            continue
            
    for fn in fourChannel_lst: 
        try:
            img = Image.open(fps + fn)

            ### Converting RGBA/CMYK to RGB
            if img.mode == 'RGBA':
                img.load() 
                new_img = Image.new("RGB", img.size, (255, 255, 255))
                new_img.paste(img, mask=img.getchannel('A'))
                new_img.save(fps + fn, quality=100)
                
            elif img.mode == 'CMYK':
                img = img.convert('RGB')
                img.save(fps + fn, quality = 100)
            
        except: 
            continue
        
    
    #Deleting the collected pics' names in the explode_lst (whose pixels are bigger than the default limit of PIL's)
    if fps.split('/')[2] == 'train_set':
        indexNames = train_df[ train_df['fname'].isin(explode_lst) ].index
        train_df = train_df.drop(indexNames).reset_index(drop=True)
        
        
    elif fps.split('/')[2] == 'valid_set':
        indexNames = valid_df[ valid_df['fname'].isin(explode_lst) ].index
        valid_df = valid_df.drop(indexNames).reset_index(drop=True)
        
    elif fps.split('/')[2] == 'test_set':
        indexNames = test_df[ test_df['fname'].isin(explode_lst) ].index
        test_df = test_df.drop(indexNames).reset_index(drop=True)
 


train_df.to_csv(output_set + 'train_set.csv', index = False)
valid_df.to_csv(output_set + 'valid_set.csv', index = False)
test_df.to_csv(output_set + 'test_set.csv', index = False)

