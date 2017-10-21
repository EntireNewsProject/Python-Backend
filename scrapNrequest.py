import requests
from newspaper import Article
import json
from json import loads, dumps
from time import sleep

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"
server = "http://entirenews.tk:3000/api/news?source=bbc"
SLEEP_TIME_IN_SEC = 1
SLEEP_TIME_IN_MILI_SEC = 0.3


def send_post_req(url, data1, params=None):
    print('send post req')
    if params is None:
        params = {'token': 'JNuhg6B7T8jhj8Y68KNKh'}  # params = { 'token': XXX }
    else:
        params['token'] = 'JNuhg6B7T8jhj8Y68KNKh'
    headers = {'content-type': 'application/json', 'Authorization': 'JNuhg6B7T8jhj8Y68KNKh'}
    request = requests.post(url, params=params, data=data1, headers=headers)
    if 200 <= request.status_code < 300:  # Response OK
        print('data posted successfully')
    else:
        json = loads(request.text)
        if 'error' in json:
            print('failed to post data, code:', request.status_code, 'message:', json['error'])
        else:
            print('failed to post data, code:', request.status_code)
    print()  # blank line


def get_text(url):
    article = Article(url)
    article.download()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    article.parse()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    return article.text  # returns the content of url passed in


def scrap_data(url):
    # somewhere in here need for loop to post
    print('scraping data started')
    req = requests.get(source + url + api)  # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text)  # reading the content (json format) from source
    if 'error'in req.text:
        print(dict_source['message'])
        print('If source is correct try replacing all space with - character')
        return
    links = []  # list used to store urls
    for article in dict_source['articles']:
        #print('scraping:', article['url'])
        dict_url = {}  # dictionary
        dict_url['url'] = article['url']  # create dictionary with -key url- and value is the link/url
        dict_url['title'] = article['title']  # add title to dictionary, same for next 3 lines
        dict_url['text'] = get_text(article['url'])
        dict_url['image'] = article['urlToImage']
        dict_url['updated'] = article['publishedAt']
        links.append(dict_url)  # combine the all the url from the dictionary created above and store them in a list call links
    print('scraping data end')
    article_dictionary = {}
    article_dictionary['source'] = url  # outer dictionary that display where the source of article came from
    article_dictionary['articles'] = links  # making the list of dictionary created above into articles value
    data = json.dumps(article_dictionary) # convert dictionary into json string or format
    #print(data)
    send_post_req(server, data, None)  # post data to server

scrap_data('bbc-news')
#        if article['publishedAt']:  # only add to dictionary if there is a published date/time