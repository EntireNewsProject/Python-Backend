import newspaper
import requests
from newspaper import Article
from json import loads, dumps

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def parse(url):
    req = requests.get(source + url + api)
    #print(req.text)
    dict = loads(req.text)

    index=0
    dic= {}
    for article in dict['articles']:
        #print(article['url'])
        scrap(article['url'])
        dic[str(index)] = article['url'] #storing all url into dictionary
        index = index + 1 # url location in dictionary
    #print(dic['1']) #an example of how to access url in dictionary
    #print('url in location 1 url stored in dic')
    #print('bottom line display dictionary string')
    #print(dic) #check if dictionary is correct
    return dic #returning the url dictionary 

def scrap(url):
    article = Article(url)
    article.download()
    article.parse()

#create function scrap then call inside of for
#store everything in dict
#after scracping convert to json
## send to node.js using request

parse('bbc-news')
parse('cnbc')
parse('cnn')

#cnn_paper = newspaper.build('http://cnn.com')
#art= requests.get(cnn_paper.articles)
#for x in art
#    print (art)
