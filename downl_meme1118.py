import praw
from psaw import PushshiftAPI
from datetime import datetime, timedelta
import requests
import urllib.request, urllib.error
import pandas as pd

df=pd.read_csv('./output/memes1118.csv')
df=df[['id','url']]

keep=[]
for ind, row in df.iterrows():
    if row.url.split(".")[-1] in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg'] or 'imgur' in row.url or 'imgflip' in row.url:
        keep.append(True)
    else:
        keep.append(False)


df=df[keep]

df.url=df.url.apply(lambda x: x.replace('/i/','/').replace('://','://i.')+'.jpg' if 'imgflip' in x and x.split(".")[-1] not in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg', 'gif']
            else x.replace('/gallery/','/').replace('://m.','://i.')+'.jpg' if '/m.' in x and 'imgur' in x and x.split(".")[-1] not in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg', 'gif']
            else x.replace('/gallery/','/').replace('://www.','://i.')+'.jpg' if '/www.' in x and 'imgur' in x and x.split(".")[-1] not in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg', 'gif']
            else x.replace('/gallery/','/').replace('://www.','://i.') if '/www.' in x and 'imgur' in x 
            else x.replace('/gallery/','/').replace('://','://i.')+'.jpg' if '//i.' not in x and 'imgur' in x and x.split(".")[-1] not in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg', 'gif']
            else x.replace('/gallery/','/')+'.jpg' if 'imgur' in x and x.split(".")[-1] not in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg', 'gif']
            else x)

df2=df

url=df2.copy()
url.columns=['image_name','image_url']

for ind, row in url.iterrows():
    row['image_name']=row['image_name']+'.'+row['image_url'].split('.')[-1]

downloaded=[]
failed=[]
import concurrent.futures
import os
import requests


def save_image_from_url(url, output_folder):
    image = requests.get(url.image_url)
    output_path = os.path.join(
        output_folder, url.image_name
    )
    with open(output_path, "wb") as f:
        f.write(image.content)

def load(df, output_folder):    
    with concurrent.futures.ThreadPoolExecutor(
    ) as executor:
        future_to_url = {
            executor.submit(save_image_from_url, url, output_folder): url
            for _, url in df.iterrows()
        }
        for future in concurrent.futures.as_completed(
            future_to_url
        ):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print(
                    "%r generated an exception: %s" % (url, exc)
                )


load(url, "./output/meme_pics/")





