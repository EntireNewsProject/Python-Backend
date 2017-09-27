import newspaper
import requests
from newspaper import Article
from json import loads, dumps

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def parse(url):
    req = requests.get(source + url + api)
    print(req.text)
    dict = loads(req.text)

    for article in dict['articles']:
        print(article['url'])


parse('bbc-news')
parse('cnbc')
parse('cnn')

#cnn_paper = newspaper.build('http://cnn.com')
#art= requests.get(cnn_paper.articles)
#for x in art
#    print (art)
