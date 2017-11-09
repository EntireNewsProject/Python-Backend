import sys
import requests
from newspaper import Article, fulltext
import json
from json import loads, dumps
from time import sleep
import re

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


def get_news(url):
    article = Article(url)
    article.download()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    article.parse()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    return article


def get_text(article):
    reg = r'(Image copyright).+'
    text = article.text  # .replace('\n\n\n','\n\n')
    matched = re.finditer(reg, text)
    for matchNum, match in enumerate(matched):
        text = text.replace(match.group(), '')
    text = text.replace('\n\n\n\n', '\n\n')
    text = text.replace('\n\n\n', '\n\n')
    # if url start with bbc
    # then check first \n
    # if it contain
    # replace \n\n\n - \n\n
    return text  # returns the content of url passed in


test = 'http://www.bbc.co.uk/news/world-asia-41840866'
get_text(get_news(test))


def get_keywords(article):
    return article.keywords


# print(get_keywords('http://www.cnn.com/2017/10/29/politics/angus-king-collusion-calls-sotu/index.html'))


def dupicate_checking(key):
    if key not in dup_key:
        dup_key.append(key)
        return True
    else:
        print('This URL has already been scraped')
        return False


def check_article_length(content):
    if len(content) < 500:
        print('This article is less than 500 characters, ignored')
        # print(content)
        return False
    else:
        return True


def scrap_data(url):
    print('scraping data started')
    req = requests.get(source + url + api)  # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text)  # reading the content (json format) from source
    # if 'error' in req.text:
    #     print('If source is correct try replacing all space with - character')
    #     return
    for article in dict_source['articles']:
        if dupicate_checking(article['url']):
            news = get_news(article['url'])
            text = get_text(news)
            if check_article_length(text):
                # print('scraping:', article['url'])
                dict_url = {}  # dictionary
                dict_url['source'] = url
                dict_url['url'] = article['url']  # create dictionary with -key url- and value is the link/url
                dict_url['title'] = article['title']  # add title to dictionary, same for next 3 lines
                dict_url['article'] = text
                dict_url['cover'] = article['urlToImage']
                dict_url['date'] = article['publishedAt']
                # dict_url['keywords'] = get_keywords(news)
                # dict_url['tags'] = get_tags(news)
                data = json.dumps(dict_url)
                print('scraping successful')
                send_post_req(server, data)
    print('scraping data end')


def save_array():
    global dup_key
    file = open('dup_key.db', 'w')
    for links in dup_key:
        file.write("%s\n" % links)
    file.close()
    print('backup done')


def read_array():
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


def main(argv):
    # argv[0]: source
    if len(argv) == 1:
        read_array()
        scrap_data(argv[0])
        save_array()
        # exit
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
