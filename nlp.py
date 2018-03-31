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

def keywords(text):
    NUM_KEYWORDS = 10
    text = split_words(text)
    if text:
        num_words = len(text)
        text = [x for x in text if x not in stopwords]
        freq = {}
        for word in text:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1

        min_size = min(NUM_KEYWORDS, len(freq))
        keywords = sorted(freq.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)
        keywords = keywords[:min_size]
        keywords = dict((x, y) for x, y in keywords)

        for k in keywords:
            articleScore = keywords[k] * 1.0 / max(num_words, 1)
            keywords[k] = articleScore
            #todo: normalize the article score
        return dict(keywords)
    else:
        return dict()

