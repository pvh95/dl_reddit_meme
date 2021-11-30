from PIL import Image
import os
from os import listdir
from os.path import isfile, join

import pandas as pd 
import numpy as np 
import tensorflow as tf

output_set = './output/'
dirname = ['train_set', 'valid_set', 'test_set']
subdirname = ['0', '1']

# Creating a list of path (6 elements) that are going to be used for reading images. It contains the train-valid-test set with their subfolders (aka their binary labels).
fullpath_sets = [str(join(output_set, dirn, subdirn + '/')) for dirn in dirname for subdirn in subdirname]


train_df = pd.read_csv(output_set + 'train_set.csv')
valid_df = pd.read_csv(output_set + 'valid_set.csv')
test_df = pd.read_csv(output_set + 'test_set.csv')


def remove_pic_from_df(df, file_lst):
    '''
    Removing pics from the corresponding dataframe
    '''
    indexNames = df[ df['fname'].isin(file_lst) ].index
    df = df.drop(indexNames).reset_index(drop=True)
    
    return df


### Deleting pixel limit exceeding images and pics with .gif extension, and converting images with color channels other than RGB
for fps in fullpath_sets:
    onlyfiles = [f for f in listdir(fps) if isfile(join(fps, f))]
    
    A_channel = list()         # A list that are going to conatin images with A(alpha) channel 
    NonA_channel = list()      # A list that are NOT going to conatin images with A(alpha) channel
    explode_lst = list()       # A list that are going to conatin images bigger than the PIL's limit pixel size, 89478485
    gif_to_delete = list()     # A list containing pics with .gif extension
    
    for pic in onlyfiles:
        
        ### Deleting .gif files from the folder 
        if pic[-3:] == 'gif': 
            gif_to_delete.append(pic)
            os.remove(fps + pic)
            continue
            
        else:  
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

                    else: #elif img.mode == 'RGB'
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
            
            file_format = fn.rsplit('.', maxsplit=1)[1].upper()
            if file_format == 'JPG': 
                file_format = 'JPEG'
                
            new_img.save(fps + fn, file_format, quality=100)
            
        except:
            continue
            
    for fn in NonA_channel: 
        try:
            img = Image.open(fps + fn)
            img = img.convert('RGB')
            
            file_format = fn.rsplit('.', maxsplit=1)[1].upper()
            if file_format == 'JPG': 
                file_format = 'JPEG'
                
            img.save(fps + fn, file_format, quality = 100)
            
        except:
            continue
        
    
    ### Removing pixel limit exceeding images and images with .gif extension from the appropriate dataframe
    if fps.split('/')[2] == 'train_set':
        train_df = remove_pic_from_df(train_df, explode_lst)
        train_df = remove_pic_from_df(train_df, gif_to_delete)
        
    elif fps.split('/')[2] == 'valid_set':
        valid_df = remove_pic_from_df(valid_df, explode_lst)
        valid_df = remove_pic_from_df(valid_df, gif_to_delete)
        
        
    elif fps.split('/')[2] == 'test_set':
        test_df = remove_pic_from_df(test_df, explode_lst)
        test_df = remove_pic_from_df(test_df, gif_to_delete)

    

### Sanity check whether all pictures are RGB and if an image cannot be decoded by tensorflow. 
for fps in fullpath_sets:
    onlyfiles = [f for f in listdir(fps) if isfile(join(fps, f))]
    
    rouge_lst = list()   ### A list of images that cannot be decoded by tensorflow or have any other flaws other than that.
    notRGB_lst = list()  ### A list of nonRGB pictures (hopefully this list will be empty in each directory after the conversion made previously)
    
    for pic in onlyfiles:
        img_raw = tf.io.read_file(fps + pic)
        
        try: 
            img_dec = tf.io.decode_image(img_raw)

        except: 
            print('-------Rouge Picture according to TF:----------')
            print('filepath:',fps)
            print('image:', pic)
            print('-----------------\n')
            rouge_lst.append(pic)
            os.remove(fps + pic)
            continue
            
            
        try:
            img = Image.open(fps + pic)
            if img.mode == 'RGB':
                continue
                
            else:
                print('######Non-RGB picture########')
                print('The non-RGB picture was found in this path:', fps + pic)
                notRGB_lst.append(pic)
                print('##############\n')

        except:
            print('-------Rouge Picture according to any other errors:----------')
            print('filepath:',fps)
            print('image:', pic)
            print('-----------------\n')
            rouge_lst.append(pic)
            os.remove(fps + pic)
            continue
            
                
    print("--------Before removing elements from the dataframe, let's summaraize------------")
    print('filepath:',fps)
    print('length of rouge_lst:', rouge_lst)
    print('length of notRGB_lst:', notRGB_lst)
    
    
    ### Removing the above mentioned images from dataframe. 
    if fps.split('/')[2] == 'train_set':
        train_df = remove_pic_from_df(train_df, rouge_lst)
        train_df = remove_pic_from_df(train_df, notRGB_lst)
        
    elif fps.split('/')[2] == 'valid_set':
        valid_df = remove_pic_from_df(valid_df, rouge_lst)
        valid_df = remove_pic_from_df(valid_df, notRGB_lst)
        
    elif fps.split('/')[2] == 'test_set':
        test_df = remove_pic_from_df(test_df, rouge_lst)
        test_df = remove_pic_from_df(test_df, notRGB_lst)
            
            


train_df.to_csv(output_set + 'train_set.csv', index = False)
valid_df.to_csv(output_set + 'valid_set.csv', index = False)
test_df.to_csv(output_set + 'test_set.csv', index = False)






