import requests
from newspaper import Article
import json
from json import loads, dumps
from time import sleep
from pathlib import Path
dup_key = []  # contain links of news sources that is already scrap
# need to automat  the scrap

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"
server = "http://entirenews.tk:3000/api/news?source=bbc-news"
SLEEP_TIME_IN_SEC = 1
SLEEP_TIME_IN_MILI_SEC = 0.3


# token is needed
def send_post_req(url, data1, params=None):
    print('send post req')
    if params is None:
        params = {'token': 'xxx'}  # params = { 'token': XXX }
    else:
        params['token'] = 'xxx'
    headers = {'content-type': 'application/json', 'Authorization': 'xxx'}
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
    # if url start with bbc
    # then check first \n
    # if it contain
    # replace \n\n\n - \n\n
    article = Article(url)
    article.download()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    article.parse()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    return article.text  # returns the content of url passed in


def dupicate_checking(key):
    if key not in dup_key:
        dup_key.append(key)
        return True
    else:
        print('This URL has already been scraped')
        return False


def scrap_data(url):
    print('scraping data started')
    req = requests.get(source + url + api)  # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text)  # reading the content (json format) from source
    if 'error' in req.text:
        print(dict_source['message'])
        print('If source is correct try replacing all space with - character')
        return
    for article in dict_source['articles']:
        # print('scraping:', article['url'])
        dict_url = {}  # dictionary
        dict_url['source'] = url
        dict_url['url'] = article['url']  # create dictionary with -key url- and value is the link/url
        dict_url['title'] = article['title']  # add title to dictionary, same for next 3 lines
        dict_url['article'] = get_text(article['url'])
        dict_url['cover'] = article['urlToImage']
        dict_url['date'] = article['publishedAt']
        # dict_url['keywords']
        # dict_url['tags']
        data = json.dumps(dict_url)
        if dupicate_checking(article['url']):
            print('test successful')
            # send_post_req(server, data)
    print('scraping data end')


def write_url_keys(data):
    directory = '././'+ '/' + 'duplicate' + '.txt'          # write file in the current directory
    with open(directory, 'a') as writefile:
        writefile.write(str(data))


def read_url_keys():
    directory = Path('././'+ '/' + 'duplicate' + '.txt')    # directory of the current path
    if directory.is_file():                         # check if file in the current directory exist
        with open(directory, 'r') as readfile:
            return readfile.read()                  # return the string/array stored in file
    else:
        f = open('././/duplicate.txt', 'w')         # create file if does not exist
        f.close()

# main function
# dup_key = read_url_keys()                           # save file string into dup key array
# scrap_data('cnbc')
# save(dup_key)


# need tags, keywords, url & date
# abc, techcrunch, bbc, bloombreg, businesinsider, buzzfeed, cnn, cnbc, hacker news, reuters, nyt, the verge, time, usa today

#        if article['publishedAt']:  # only add to dictionary if there is a published date/time
