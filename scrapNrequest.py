import requests
from json import loads, dumps

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"

def fetch_source(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        dic[str(index)] = article['url'] #storing all url into dictionary
        index = index + 1 # url location in dictionary
    return dic #returning the url dictionary

def fetch_titles(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        dic[str(index)] = article['title']
        index = index + 1
    return dic

def fetch_description(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        dic[str(index)] = article['description']
        index = index + 1
    return dic

def fetch_datetime(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        if article['publishedAt']: #only add to dictionary if there is a published date/time
            dic[str(index)] = article['publishedAt']
            index = index + 1
    return dic

#create function scrap then call inside of for
#store everything in dict
#after scracping convert to json
## send to node.js using request

#cnn_paper = newspaper.build('http://cnn.com')
#art= requests.get(cnn_paper.articles)
