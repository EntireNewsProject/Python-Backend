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
    return article.text  # returns the content of url passed in


scrap_content('http://www.cnn.com/2017/10/04/us/paddock-profile-house-cash-fence-invs/index.html')


def fetch_content(url):
    req = requests.get(source + url + api)  # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text) # reading the content (json format) from source
    links = [] # list used to store urls
    for article in dict_source['articles']:
        dict_url = {} #dictionary
        dict_url['url'] = article['url'] # create dictionary with -key url- and value is the link/url
        links.append(dict_url)  # combine the all the url from the dictionary created above and store them in a list call links
    jlink = [] # list used to store url and text dictionary
    for descrip in links:
        dic_text = {} 
        dic_text['text'] = scrap_content(descrip['url']) # scrap content from url that was saved in links(above)
        jlink.append(descrip) # add {url: value}
        jlink.append(dic_text) # add {text: value}
    return jlink  # list that contain [{url: value}, {text:value}] formatted like this for converting to json format


print(
    '-----------------------------------------------------------------------------------------------------------------------------------')
live_data = fetch_content('cnn')
print('--------------------------------------------------------------------')


def convert2json(dir, name, data):
    directory = './' + dir + '/' + name + '.json'
    with open(directory, 'w') as filejson:
        json.dump(data, filejson)

# convert2json('./','example2',live_data)



#        if article['publishedAt']:  # only add to dictionary if there is a published date/time

# create function scrap then call inside of for
# store everything in dict
# after scracping convert to json
## send to node.js using request
