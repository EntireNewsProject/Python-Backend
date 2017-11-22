import sys
import requests
from newspaper import Article, fulltext
import json
from json import loads, dumps
from time import sleep
import re

URL_API = 'http://listeapp.tk/api'
TOKEN = ''

dup_key = []  # contain links of news sources that is already scrap

source = "https://newsapi.org/v1/articles?source="
api = "&apiKey=4b6587f8cd2149e9916c4705ad524c3a"
server = "http://entirenews.tk:3000/api/news?source=bbc-news"
SLEEP_TIME_IN_SEC = 1
SLEEP_TIME_IN_MILI_SEC = 0.3

# token is needed
def send_post_req(url, data1, params=None):
    print('send post req')
    if params is None:
        params = {'token': 'xxx'}                # params = { 'token': XXX }
    else:
        params['token'] = 'xxx'
    headers = {'content-type': 'application/json', 'Authorization': 'xxx'}
    request = requests.post(url, params=params, data=data1, headers=headers)
    if 200 <= request.status_code < 300:         # Response OK
        print('data posted successfully')
    else:
        json = loads(request.text)
        if 'error' in json:
            print('failed to post data, code:', request.status_code, 'message:', json['error'])
        else:
            print('failed to post data, code:', request.status_code)
    print()  # blank line


def get_news(url):                               # Scraping of articles from provided source
    article = Article(url)
    article.download()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    article.parse()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    return article


def replace_extra_line(texts):
    texts = texts.replace('\n\n\n\n', '\n\n')    # replacing extra lines with just double line spacing
    texts = texts.replace('\n\n\n', '\n\n')
    return texts


def get_text(article):
    text = replace_extra_line(article.text)
    text = text.replace('Media playback is unsupported on your device Media caption ','')
    return text


def replace_text(article):                  # function replace the sentence that start with Image copyright with blank
    reg = r'(Image copyright).+'
    text = article
    matched = re.finditer(reg, text)
    for matchNum, match in enumerate(matched):
        text = text.replace(match.group(), '')
    text = replace_extra_line(text)
    return text


def get_keywords(article):
    return article.keywords


def dupicate_checking(key):
    if key not in dup_key:
        dup_key.append(key)                 # Save url into dup_key list for storing later
        return True
    else:
        print('This URL has already been scraped')
        return False


def check_article_length(content):          # Only post articles that have more than 500 character in them
    if len(content) < 500:
        print('This article is less than 500 characters, ignored')
        return False
    else:
        return True


def scrap_data(url):
    print('scraping data started')
    req = requests.get(source + url + api)      # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text)               # reading the content (json format) from source
    if req.status_code == 400:                  # If unable to find source then exit
        print('Source is incorrect or try replacing all spaces with " - " character')
        return
    for article in dict_source['articles']:
        if dupicate_checking(article['url']):
            news = get_news(article['url'])
            text = get_text(news)
            if url == 'bbc-news':
                text = replace_text(text)
            if check_article_length(text):
                # print('scraping:', article['url'])
                dict_url = {}  # dictionary
                dict_url['source'] = url                        # name of source where articles are getting scraped from
                dict_url['url'] = article['url']                # add ['name'] to dictionary, same for next 4 lines
                dict_url['title'] = article['title']
                dict_url['article'] = text
                dict_url['cover'] = article['urlToImage']
                dict_url['date'] = article['publishedAt']
                # dict_url['keywords'] = get_keywords(news)
                # dict_url['tags'] = get_tags(news)
                data = json.dumps(dict_url)
                send_post_req(server, data)
                print('Posting article done')
    print('scraping data end')


def save_array():                               # save url string
    global dup_key
    file = open('dup_key.db', 'w')
    for links in dup_key:
        file.write("%s\n" % links)
    file.close()
    print('backup done')


def read_array():                               # read stored url string
    global dup_key
    try:
        file = open('dup_key.db', 'r')
    except IOError:
        print('backup not found, ignored')
    else:
        with file:
            dup_key = file.read().splitlines()
            file.close()
            print('read backup successfully')


def req_login(username, password):
    print('logging in...')
    url = URL_API + '/login'
    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}
    request = requests.post(url, data=dumps(payload), headers=headers)
    if request.status_code == 200:
        print('logged in successfully as:', request.json()['user']['_id'])
        print('received new token from server')
        global TOKEN
        TOKEN = request.json()['token']
        file = open('token.txt', 'w')
        file.write(TOKEN)
        file.close()
        print('token updated')
    else:
        print('failed to logged in, status code:', request.status_code)
        # print(request.json())


def req_me():
    print('get me...')
    url = URL_API + '/me'
    global TOKEN
    headers = {'content-type': 'application/json', 'Authorization': TOKEN}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        print('received new token from server')
        TOKEN = request.json()['token']
        file = open('token.txt', 'w')
        file.write(TOKEN)
        file.close()
        print('token updated')
    else:
        print('token expired...')
        req_login('entirenews_py', '123456')


def read_token():
    print('read saved token...')
    global TOKEN
    try:
        file = open('token.txt', 'r')
    except IOError:
        print('token not found, requesting new token')
        req_login('entirenews_py', '123456')
    else:
        with file:
            TOKEN = file.read()
            file.close()
            print('read token successful')
            req_me()

            

def main(argv):
    if len(argv) == 1:
        read_token()
        read_array()
        scrap_data(argv[0])                     # argv[0]: source
        save_array()
    else:
        print('RuntimeError: incorrect number of args')
        sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])

# run like
# python scrapNrequest.py bloomberg
# python scrapNrequest.py business-insider
# etc.

# scrap_data('bbc-news')
# scrap_data('bloomberg')
# scrap_data('business-insider')
# scrap_data('buzzfeed')
# scrap_data('cnn')
# scrap_data('cnbc')
# scrap_data('engadget')
# scrap_data('espn')
# scrap_data('hacker-news')
# scrap_data('reuters')
# scrap_data('techcrunch')
# scrap_data('techradar')
# scrap_data('the-new-york-times')
# scrap_data('the-verge')
# scrap_data('time')
# scrap_data('usa-today')
