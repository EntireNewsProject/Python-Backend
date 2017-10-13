import requests
from newspaper import Article
import json
from json import loads, dumps

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"


def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text  # returns the content of url passed in


def scrap_data(url):
    req = requests.get(source + url + api)  # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text)  # reading the content (json format) from source
    links = []  # list used to store urls
    for article in dict_source['articles']:
        dict_url = {}  # dictionary
        dict_url['url'] = article['url']  # create dictionary with -key url- and value is the link/url
        dict_url['title'] = article['title']  # add title to dictionary, same for next 3 lines
        dict_url['text'] = get_text(article['url'])
        dict_url['image'] = article['urlToImage']
        dict_url['updated'] = article['publishedAt']
        links.append(dict_url)  # combine the all the url from the dictionary created above and store them in a list call links
    article_dictionary = {}
    article_dictionary['source'] = url  # outer dictionary that display where the source of article came from
    article_dictionary['articles'] = links  # making the list of dictionary created above into articles value
    return article_dictionary  # return dictionary that contain [{url: value}, {text:value}] formatted like this for converting to json format


def convert2json(dir, name, data):  # function to write/saved json file
    directory = './' + dir + '/' + name + '.json'  # ./ is to saved .json file to current directory
    with open(directory, 'w') as filejson:
        json.dump(data, filejson)


live_data = scrap_data('cnn')  # save scraped information into variable

convert2json('./', 'example', live_data)  # output real articles data in json format to a .json file name example

# make one list of dictionaryS and inside those dictionaryS have 5 key url, title, text, date, and image
# i need to do dictionary with key that has a dictionary value exampe dict {article: {url: value, text: value, etc}}

#        if article['publishedAt']:  # only add to dictionary if there is a published date/time

# create function scrap then call inside of for
# store everything in dict
# after scracping convert to json
## send to node.js using request
