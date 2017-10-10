import requests
from newspaper import Article
import json
from json import loads

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def scrap_content(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def fetch_content(url):
    req = requests.get(source + url + api)
    dict_source = loads(req.text)
    dict_result = []
    for article in dict_source['articles']:
        dict_result.append(article['url'])  # add all url links from the api source dictionary into dict_result as a list

    text = []
    for text_source in dict_result:
        text.append(scrap_content(text_source))  # put all article's text into a list call text
    s={}
    dic_text = {}
    index = 0
    dic = []
    for descrip in text:
        dic_text['text'] = descrip
        s[str(index)] = dic_text
        print(s)
        dic.append(s)
        index += 1

    return dic  # return the list of articles text content
print('-----------------------------------------------------------------------------------------------------------------------------------')
data= fetch_content('cnn')
print('--------------------------------------------------------------------')
#print(data)
def convert2json(dir, name, data):
    directory = './' + dir + '/' + name + '.json'
    with open(directory,'w') as filejson:
        json.dump(data, filejson)

    #convert2json('./','example', )


#        if article['publishedAt']:  # only add to dictionary if there is a published date/time

# create function scrap then call inside of for
# store everything in dict
# after scracping convert to json
## send to node.js using request
