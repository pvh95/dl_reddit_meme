import os
import praw
from psaw import PushshiftAPI
from datetime import datetime, timedelta
import requests
import urllib.request, urllib.error


reddit = praw.Reddit(client_id = 'YOUR-ID', 
                     client_secret = 'YOUR_SECRET_ID', 
                     user_agent = 'USER_AGENT')

reddit=PushshiftAPI(reddit)


def download_memes(start,end):
    start_date=start
    end_date=end


    save_path = './output/meme_pics'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    while True:
        t=0
        generator = reddit.search_submissions(limit=250,
                                      subreddit='memes',
                                      after=int(start_date.timestamp()),
                                      before=int((start_date+timedelta(days=1)).timestamp()))
        for post in generator:
            try: 
                temp_var = urllib.request.urlopen(post.url)
                
            except:
                continue
                
            #except urllib.error.HTTPError as httpErr:
                #print(post.url)
                #print('HTTP', httpErr.code, 'ERROR \n')
                #continue
            
            #except urllib.error.URLError as urlErr:
                #print(post.url)
                #print('URL', urlErr.reason, 'ERROR \n')
                #continue
                
                
            try:
                img_data = requests.get(post.url).content
                if post.url[-3:] in ['jpg', 'png', 'bmp', 'jpeg', 'tiff', 'svg']:
                    if post.selftext.replace(";",",") == '[deleted]': 
                        continue
                    #print(post.url, '\n')
                    if (requests.get(post.url).url == 'https://i.imgur.com/removed.png') or (requests.get(post.url).url == 'http://www.noelshack.com/'):
                        continue
                    #print(post.selftext.replace(";",","))
                    file_name = f'{datetime.strftime(start_date,"%Y.%m.%d")}_{t}.png'
                    path = os.path.join(save_path, file_name)
                    with open(path, 'wb') as handler:
                        handler.write(img_data)
                        
                    with open('./output/memes.csv','a') as fd:
                        fd.write(f'"{datetime.strftime(start_date,"%Y.%m.%d")}_{t}";"{post.title.replace(";",",")}";"{post.selftext.replace(";",",")}";{str(post.score).strip()}\n')
                        #fd.write(f'"{datetime.strftime(start_date,"%Y.%m.%d")}_{t}";"{post.title.replace(";",",")}";{str(post.score).strip()}\n')
                    t+=1
                    
                else: 
                    continue 
            except:
                continue
        start_date=start_date+timedelta(days=1)
        if start_date==end_date:
            break


download_memes(datetime.strptime('2011.10.02.', '%Y.%m.%d.'), datetime.strptime('2021.10.17.', '%Y.%m.%d.'))





