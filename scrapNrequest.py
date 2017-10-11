import requests
from newspaper import Article
import json
from json import loads, dumps

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def scrap_content(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text
scrap_content('http://www.cnn.com/2017/10/04/us/paddock-profile-house-cash-fence-invs/index.html')
def fetch_content(url):
    req = requests.get(source + url + api)
    dict_source = loads(req.text)
    links = []
    for article in dict_source['articles']:
        dict_url = {}
        dict_url ['url'] = article['url']
        links.append(dict_url) # put all article's text into a list call text
    jlink = []
    for descrip in links:
        dic_text = {}
        dic_text['text'] = scrap_content(descrip['url'])
        jlink.append(descrip)
        jlink.append(dic_text)
    return jlink # return the list of articles text content
print('-----------------------------------------------------------------------------------------------------------------------------------')
live_data = fetch_content('cnn')
print('--------------------------------------------------------------------')

def convert2json(dir, name, data):
    directory = './' + dir + '/' + name + '.json'
    with open(directory,'w') as filejson:
        json.dump(data, filejson)
#convert2json('./','example2',live_data)



#        if article['publishedAt']:  # only add to dictionary if there is a published date/time

# create function scrap then call inside of for
# store everything in dict
# after scracping convert to json
## send to node.js using request
