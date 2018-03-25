import re

import settings

#Preparing for keyword function

def split_words(text):
    try:
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None

def load_stopwords():
    global stopwords
    stopwordsFile = settings.NLP_STOPWORDS_EN
    with open(stopwordsFile, 'r', encoding='utf-8') as f:
        stopwords.update(set([w.strip() for w in f.readlines()]))