import requests
from newspaper import Article
from json import loads, dumps
from bs4 import BeautifulSoup

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def fetch_titles(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        #print(article['url'])
        dic[str(index)] = article['title']
        index = index + 1
    return dic

def fetch_source(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        #print(article['url'])
        dic[str(index)] = article['url'] #storing all url into dictionary
        index = index + 1 # url location in dictionary
    #print(dic['1']) #an example of how to access url in dictionary
    #print('url in location 1 url stored in dic')
    #print('bottom line display dictionary string')
    #print(dic) #check if dictionary is correct
    return dic #returning the url dictionary

def fetch_description(url):
    req = requests.get(source + url + api)
    dict = loads(req.text)
    index=0
    dic= {}
    for article in dict['articles']:
        #print(article['url'])
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
#print(fetch_datetime('cnn'))

#print(fetch_titles('cnn'))

#print (article_links('bbc-news'))

#print(article_title('cnn'))

#create function scrap then call inside of for
#store everything in dict
#after scracping convert to json
## send to node.js using request


#fetch_source('cnbc')
#fetch_source('cnn')

#cnn_paper = newspaper.build('http://cnn.com')
#art= requests.get(cnn_paper.articles)
#for x in art
#    print (art)
