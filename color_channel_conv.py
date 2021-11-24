from PIL import Image
import os
from os import listdir
from os.path import isfile, join

import pandas as pd 
import numpy as np 


output_set = './output/'
dirname = ['train_set', 'valid_set', 'test_set']
subdirname = ['0', '1']
# Creating a list of path (6 elements) that are going to be used for reading images. It contains the train-valid-test set with their subfolders (aka their binary labels).
fullpath_sets = [str(join(output_set, dirn, subdirn + '/')) for dirn in dirname for subdirn in subdirname]   


train_df = pd.read_csv(output_set + 'train_set.csv')
valid_df = pd.read_csv(output_set + 'valid_set.csv')
test_df = pd.read_csv(output_set + 'test_set.csv')

### Deleting pixel limit exceeding images and converting images with color channels other than RGB
for fps in fullpath_sets:
    onlyfiles = [f for f in listdir(fps) if isfile(join(fps, f))]
    
    A_channel = list()  # A list that are going to conatin images with A(alpha) channel 
    NonA_channel = list() # A list that are NOT going to conatin images with A(alpha) channel 
    explode_lst = list()  # A A list that are going to conatin images bigger than the PIL's limit pixel size, 89478485
    
    for pic in onlyfiles:
        try:
            img = Image.open(fps + pic)
            ### Throwing out images bigger than the PIL's limit pixel size, 89478485 and collect those pictures into the 'explode_lst'
            if img.size[0] * img.size[1] > 89478485:  
                explode_lst.append(pic)
                os.remove(fps + pic)
                continue

            else:
                ### Collecting images with color channels other than RGB (such as CMYK, RGBA, P, L, LA) to their respective A_channel or NonA_channel list
                image_mode = img.mode
                if (image_mode != 'RGB') and ('A' not in image_mode):
                    NonA_channel.append(pic)
                
                elif (image_mode != 'RGB') and ('A' in image_mode):
                    A_channel.append(pic)
                
                else: #img.mode == 'RGB'
                    continue

        except: 
            continue

    ### Converting images with color channels other than RGB (such as CMYK, RGBA, P, L, LA) to RGB from A_channel or NonA_channel list         
    for fn in A_channel: 
        try:
            img = Image.open(fps + fn)
            img.load() 
            new_img = Image.new("RGB", img.size, (255, 255, 255))
            new_img.paste(img, mask=img.getchannel('A'))
            new_img.save(fps + fn, quality=100)
            
        except: 
            continue
            
    for fn in NonA_channel: 
        try:
            img = Image.open(fps + fn)
            img = img.convert('RGB')
            img.save(fps + fn, quality = 100)
            
        except: 
            continue
        
    ### Removing pixel limit exceeding images from the appropriate dataframe
    if fps.split('/')[2] == 'train_set':
        indexNames = train_df[ train_df['fname'].isin(explode_lst) ].index
        train_df = train_df.drop(indexNames).reset_index(drop=True)
        
        
    elif fps.split('/')[2] == 'valid_set':
        indexNames = valid_df[ valid_df['fname'].isin(explode_lst) ].index
        valid_df = valid_df.drop(indexNames).reset_index(drop=True)
        
    elif fps.split('/')[2] == 'test_set':
        indexNames = test_df[ test_df['fname'].isin(explode_lst) ].index
        test_df = test_df.drop(indexNames).reset_index(drop=True)
 


### Deleting gif files
for fps in fullpath_sets:
    onlyfiles = [f for f in listdir(fps) if isfile(join(fps, f))]
    gif_to_delete = list() 
    
    for pic in onlyfiles:
        if pic[-3:] == 'gif': 
            gif_to_delete.append(pic)
            os.remove(fps + pic)
            
    print(fps)
    print('In fps the length of gif_to_delete is:', len(gif_to_delete))
    print('--------\n')


    ### Removing gif images from the appropriate dataframes
    if fps.split('/')[2] == 'train_set':
        indexNames = train_df[ train_df['fname'].isin(gif_to_delete) ].index
        train_df = train_df.drop(indexNames).reset_index(drop=True)
        
        
    elif fps.split('/')[2] == 'valid_set':
        indexNames = valid_df[ valid_df['fname'].isin(gif_to_delete) ].index
        valid_df = valid_df.drop(indexNames).reset_index(drop=True)
        
    elif fps.split('/')[2] == 'test_set':
        indexNames = test_df[ test_df['fname'].isin(gif_to_delete) ].index
        test_df = test_df.drop(indexNames).reset_index(drop=True)

    

train_df.to_csv(output_set + 'train_set.csv', index = False)
valid_df.to_csv(output_set + 'valid_set.csv', index = False)
test_df.to_csv(output_set + 'test_set.csv', index = False)

