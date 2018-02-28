import requests
import json
import urllib.parse
import configparser
import pandas as pd
from datetime import date
from datetime import timedelta


def get_news(start_date=date.today(), end_date=date.today()):
    config = configparser.ConfigParser()
    config.read("newsapi_config.ini")

    key = config['newsapi']['key']
    url = 'https://newsapi.org/v2/everything?'
    delta = (end_date - start_date).days + 1
    result = []
    for cur_date in (start_date + timedelta(n) for n in range(0, delta)):
        params = {'q': 'bitcoin', 'language': 'en',
                  'from': cur_date.isoformat(), 'to': cur_date.isoformat(), 'apiKey': key}
        built_url = url + urllib.parse.urlencode(params)
        response = requests.get(built_url).json()
        result = result + response['articles']
    return result


def process_news(articles):
    result = pd.read_json(json.dumps(articles))
    print(result.size)
    return result

def add_marks(artcles):
    for index, row in artcles.iterrows():
        if pd.isnull(row['mark']):
            print(row['title'])
            print(row['description'])
            print('your mark: ')
            mark = input()
            if mark == 'exit':
                return
            row['mark'] = mark
            print(row)
            print(index)
            artcles[index] = row


# news = get_news(start_date=date.today() - timedelta(50), end_date=date.today() - timedelta(10))
# processed_news = process_news(news)
# processed_news['mark'] = np.nan
processed_news = pd.read_csv('news.csv')
add_marks(processed_news)
processed_news.to_csv('news.csv')
#add_marks(processed_news)
