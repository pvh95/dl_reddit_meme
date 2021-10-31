import os
import pandas as pd
import requests
import json
import time
import dateutil
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


### Determining the time interval using for downloading headlines from NYT 

start = datetime.date(2011, 10, 1)
end = datetime.date.today()

print('Start date: ' + str(start))
print('End date: ' + str(end))



''' A list of months that falls beetween start = 2011-10-01 and end = today. 
Necesseary for Archive API as it functions on one month only '''

months = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]



def send_request(date):
    '''Sending a request to the NYT Archive API for given date. 
    Two rate limits: 4,000 requests per day and 10 requests per minute. 
    You should sleep 6 seconds between calls to avoid hitting the per minute rate limit'''
    
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + 'YOUR_KEY'
    
    try:
        response = requests.get(url, verify=False).json()
    except Exception:
        return None
    time.sleep(6)
    return response


def is_valid(article, date):
    ''' Checking whether an article has a headline and its publication date 
    falls beetween the intended time range'''
    
    is_in_range = date > start and date < end
    has_headline = ( type(article['headline']) == dict and 'main' in article['headline'].keys() ) 
    
    return (is_in_range) and (has_headline)


def parse_response(response):
    '''Parses and returns response as pandas data frame.'''
    
    ### Setting up a data dictionary for getting the details of articles for a month in question 
    data = {'headline': [],  
        'date': [], 
        'doc_type': [],
        'material_type': [],
        'section': [],
        'keywords': []}
    
    articles = response['response']['docs'] 
    
    for article in articles: 
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
            if 'section' in article:
                data['section'].append(article['section_name'])
            else:
                data['section'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article: 
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
            
    return pd.DataFrame(data) 


def get_data(dates):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    unified_df = None 
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    
    if not os.path.exists('./output/headlines'):
        os.mkdir('./output/headlines')
        
    for date in dates:
        print('Working on ' + str(date) + '...')
        csv_path = './output/headlines/' + date[0] + '-' + date[1] + '.csv'
        unified_csv_path = './output/unified_headlines.csv'
        if not os.path.exists(csv_path): # If we don't already have this month 
            response = send_request(date)
            if response is not None:
                df = parse_response(response)
                unified_df = pd.concat([unified_df, df])
                total += len(df)
                df.to_csv(csv_path, index=False)
                print('Saving ' + csv_path + '...')
                
    unified_df.to_csv(unified_csv_path, index=False)
    
    print('Number of articles collected: ' + str(total))


get_data(months)

