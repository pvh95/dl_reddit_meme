import praw
from psaw import PushshiftAPI
from datetime import datetime, timedelta
import requests
import urllib.request, urllib.error
import pandas as pd


df=pd.DataFrame(columns=['id','title','text','score','num_comments','url'])



reddit = praw.Reddit(client_id = 'YOUR-ID', 
                     client_secret = 'YOUR_SECRET_ID', 
                     user_agent = 'USER_AGENT')

reddit=PushshiftAPI(reddit)



def download_memes(start,end):
    start_date=start
    end_date=end
    global df
    while True:
        t=0
        generator = reddit.search_submissions(limit=200,
                                      subreddit='memes',
                                      after=int(start_date.timestamp()),
                                      before=int((start_date+timedelta(days=1)).timestamp()))
        for post in generator:
          try:
            df=df.append({'id':f'{datetime.strftime(start_date,"%Y.%m.%d")}_{t}',
                          'title':post.title,
                          'text':post.selftext,
                          'score':post.score,
                          'num_comments':post.num_comments,
                          'url':post.url}, ignore_index=True)
            t+=1
          except:
            print(t)
            continue
        start_date=start_date+timedelta(days=1)
        if start_date==end_date:
            break



download_memes(datetime.strptime('2011.01.01.', '%Y.%m.%d.'), datetime.strptime('2019.01.01.', '%Y.%m.%d.'))


df.to_csv('./output/memes1118.csv', index = False)






