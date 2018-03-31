import re
import math

import settings


ideal = 20.0

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
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords)
    else:
        return dict()


def split_sentences(text):
    import nltk.data
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    sentences = [x.replace('\n', '') for x in sentences if len(x) > 10]
    return sentences

def length_score(sentence_len):
    return 1 - math.fabs(ideal - sentence_len) / ideal


def title_score(title, sentence):
    if title:
        title = [x for x in title if x not in stopwords]
        count = 0.0
        for word in sentence:
            if (word not in stopwords and word in title):
                count += 1.0
        return count / max(len(title), 1)
    else:
        return 0
        #todo: sentence positioning and the score function

def sentence_position(i, size):
    normalized = i * 1.0 / size
    if (normalized > 1.0):
        return 0
    elif (normalized > 0.9):
        return 0.15
    elif (normalized > 0.8):
        return 0.04
    elif (normalized > 0.7):
        return 0.04
    elif (normalized > 0.6):
        return 0.06
    elif (normalized > 0.5):
        return 0.04
    elif (normalized > 0.4):
        return 0.05
    elif (normalized > 0.3):
        return 0.08
    elif (normalized > 0.2):
        return 0.14
    elif (normalized > 0.1):
        return 0.23
    elif (normalized > 0):
        return 0.17
    else:
        return 0
