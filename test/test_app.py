"""
Entire News - Python Scrapper and NLP unit tests.
"""
import sys
import os
import unittest

# from collections import defaultdict, OrderedDict
# import concurrent.futures

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')


sys.path.insert(0, PARENT_DIR)

TEXT_FN = os.path.join(TEST_DIR, 'data', 'text')
HTML_FN = os.path.join(TEST_DIR, 'data', 'html')
URLS_FILE = os.path.join(TEST_DIR, 'data', 'fulltext_url_list.txt')

# import newspaper
# from newspaper import app, nlp
# from newspaper import Article, fulltext, Source, ArticleException, news_pool
# from newspaper.configuration import Configuration
# from newspaper.urls import get_domain

class ExhaustiveFullTextCase(object):
    pass


def check_url(*args, **kwargs):
    return ExhaustiveFullTextCase.check_url(*args, **kwargs)




if __name__ == '__main__':
    argv = list(sys.argv)
    if 'fulltext' in argv:
        argv.remove('fulltext')  # remove it here, so it doesn't pass to unittest

    unittest.main(verbosity=0, argv=argv)