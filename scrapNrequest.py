import requests
from newspaper import Article
from json import loads, dumps

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def scrap_content(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def fetch_source(url):
    req = requests.get(source + url + api)
    dict_source = loads(req.text)
    dict_result = []
    for article in dict_source['articles']:
        dict_result.append(article['url'])  # add all url links from the api source dictionary into dict_result as a list
    text = []
    for text_source in dict_result:
        text.append(scrap_content(text_source)) #put all article's text into a list call text
    return text # return the list of articles text content

def function_testing(url):
    x = fetch_source(url)
    print(x[0])

function_testing('cnn')
print('---------------------------------------------------------')
print('')
function_testing('bbc-news')


def send_req():
    pass

#        if article['publishedAt']:  # only add to dictionary if there is a published date/time

# create function scrap then call inside of for
# store everything in dict
# after scracping convert to json
## send to node.js using request
