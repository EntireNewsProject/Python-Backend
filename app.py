import requests
from newspaper import Article
import json
from json import loads, dumps
from time import sleep
import re
import schedule
import time
import nlp as np

# URL_API = 'http://entirenews.tk:3000'
URL_API = 'http://localhost:3000'
TOKEN = ''
DUPLICATE_KEYS = []  # contain links of news sources that is already scrap
URL_NEWAPI = "https://newsapi.org/v1/articles?source="
API_KEY = "&apiKey=310673ab67a84347a95ca7db86288f38"
# SOURCES = {'bbc-news', 'bloomberg', 'business-insider', 'buzzfeed', 'cnbc', 'cnn', 'engadget', 'espn', 'hacker-news',
#            'techcrunch', 'techradar', 'the-new-york-times', 'the-verge', 'time', 'usa-today'}
# SOURCES = {'business-insider', 'cnbc', 'engadget', 'espn',
#            'hacker-news', 'techradar', 'the-verge', 'time', 'usa-today'}
SOURCES = {'bbc-news', 'bloomberg', 'buzzfeed', 'cnn', 'techcrunch', 'the-new-york-times'}
SLEEP_TIME_IN_SEC = 1
SLEEP_TIME_IN_MILI_SEC = 0.3


# token is needed
def send_post_req(url, data, params=None):
    print('send post req')
    if params is None:
        params = {}
        url = URL_API + url
    headers = {'content-type': 'application/json', 'Authorization': TOKEN}
    request = requests.post(url, params=params, data=data, headers=headers)
    if 200 <= request.status_code < 300:  # Response OK
        print('data posted successfully')
    else:
        json = loads(request.text)
        if 'error' in json:
            print('failed to post data, code:', request.status_code, 'message:', json['error'])
        else:
            print('failed to post data, code:', request.status_code)
    print()  # blank line


def get_news(url):  # Scraping of articles from provided source
    article = Article(url)
    article.download()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    article.parse()
    sleep(SLEEP_TIME_IN_MILI_SEC)
    return article


def replace_extra_line(texts):
    texts = texts.replace('\n\n\n\n', '\n\n')  # replacing extra lines with just double line spacing
    texts = texts.replace('\n\n\n', '\n\n')
    return texts


def get_text(article):
    text = replace_extra_line(article.text)
    text = text.replace('Media playback is unsupported on your device Media caption ', '')
    return text


def replace_text(article):  # function replace the sentence that start with Image copyright with blank
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
    if key not in DUPLICATE_KEYS:
        DUPLICATE_KEYS.append(key)  # Save url into dup_key list for storing later
        return True
    else:
        print('This URL has already been scraped')
        return False


def check_article_length(content):  # Only post articles that have more than 500 character in them
    if len(content) < 500:
        print('This article is less than 500 characters, ignored')
        return False
    else:
        return True


def nlp(dict_url):
    np.load_stopwords()
    text_keyws = list(np.keywords(dict_url['article']).keys())
    title_keyws = list(np.keywords(dict_url['title']).keys())
    keyws = list(set(title_keyws + text_keyws))
    dict_url['keywords'] = keyws
    max_sents = 5

    summary_sents = np.summarize(dict_url['title'], dict_url['article'], max_sents)
    summary = '\n'.join(summary_sents)
    dict_url['summary'] = summary
    return dict_url


def scrap_data(url):
    print('scraping data started')
    req = requests.get(URL_NEWAPI + url + API_KEY)  # getting articles from source for example: cnn, bbc-news, cnbc, etc
    dict_source = loads(req.text)  # reading the content (json format) from source
    print(dict_source)
    if req.status_code == 400:  # If unable to find source then exit
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
                dict_url['source'] = url  # name of source where articles are getting scraped from
                dict_url['url'] = article['url']  # add ['name'] to dictionary, same for next 4 lines
                dict_url['title'] = article['title']
                dict_url['article'] = text
                dict_url['cover'] = article['urlToImage']
                dict_url['date'] = article['publishedAt']
                print(dict_url)
                dict_url = nlp(dict_url)
                print(dict_url)
                # dict_url['keywords'] = get_keywords(news)
                # dict_url['tags'] = get_tags(news)
                data = json.dumps(dict_url)
                send_post_req('/api/news', data)
                print('Posting article done')
    print('scraping data end')


def save_array():  # save url string
    global DUPLICATE_KEYS
    file = open('dup_key.db', 'w')
    for links in DUPLICATE_KEYS:
        file.write("%s\n" % links)
    file.close()
    print('backup done')


def read_array():  # read stored url string
    global DUPLICATE_KEYS
    try:
        file = open('/home/ubuntu/apps/python/dup_key.db', 'r')
    except IOError:
        print('backup not found, ignored')
    else:
        with file:
            DUPLICATE_KEYS = file.read().splitlines()
            file.close()
            print('read backup successfully')


def req_login(username, password):
    print('logging in...')
    url = URL_API + '/user/login'
    payload = {'username': username, 'password': password}
    headers = {'content-type': 'application/json'}
    request = requests.post(url, data=dumps(payload), headers=headers)
    if request.status_code == 200:
        print('logged in successfully')
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
    url = URL_API + '/user/authenticate'
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


def job():
    # read_token()
    read_array()
    for src in SOURCES:
        scrap_data(src)
    save_array()


#schedule.every(20).minutes.do(job)

if __name__ == '__main__':
    while 1:
        #schedule.run_pending()
        #time.sleep(1)
        job()