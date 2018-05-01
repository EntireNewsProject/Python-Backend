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


def print_test(method):


    def run(*args, **kw):
        ts = time.time()
        print('\ttesting function %r' % method.__name__)
        method(*args, **kw)
        te = time.time()
        print('\t[OK] in %r %2.2f sec' % (method.__name__, te - ts))

    return run

@unittest.skipIf('fulltext' not in sys.argv, 'Skipping fulltext tests')
class ExhaustiveFullTextCase(unittest.TestCase):
    @staticmethod
    def check_url(args):
        """
        :param (basestr, basestr) url, res_filename:
        :return: (pubdate_failed, fulltext_failed)
        """
        url, res_filename = args
        pubdate_failed, fulltext_failed = False, False
        html = mock_resource_with(res_filename, 'html')
        try:
            a = Article(url)
            a.download(html)
            a.parse()
            if a.publish_date is None:
                pubdate_failed = True
        except Exception:
            print('<< URL: %s parse ERROR >>' % url)
            traceback.print_exc()
            pubdate_failed, fulltext_failed = True, True
        else:
            correct_text = mock_resource_with(res_filename, 'txt')
            if not (a.text == correct_text):
                print('%s -- %s -- %s' %
                      ('Fulltext failed',
                       res_filename, correct_text.strip()))
                fulltext_failed = True
        return pubdate_failed, fulltext_failed


def get_news(*args, **kwargs):
    return ExhaustiveFullTextCase.check_url(*args, **kwargs)

def mock_resource_with(filename, resource_type):
    """
    checks requests and downloads
    """
    VALID_RESOURCES = ['html', 'txt']
    if resource_type not in VALID_RESOURCES:
        raise Exception('Mocked resource must be one of: %s' %
                        ', '.join(VALID_RESOURCES))
    subfolder = 'text' if resource_type == 'txt' else 'html'
    resource_path = os.path.join(TEST_DIR, "data/%s/%s.%s" %
                                 (subfolder, filename, resource_type))
    with open(resource_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_base_domain(url):

        domain = get_domain(url)
        tld = '.'.join(domain.split('.')[-2:])
        if tld in ['co.uk', 'com.au', 'au.com']:  # edge cases
            end_chunks = domain.split('.')[-3:]
        else:
            end_chunks = domain.split('.')[-2:]
        base_domain = '.'.join(end_chunks)
        return base_domain


# TODO: assert statements are commented out for full-text


if __name__ == '__main__':
    argv = list(sys.argv)
    if 'fulltext' in argv:
        argv.remove('fulltext')  # remove it here, so it doesn't pass to unittest

    unittest.main(verbosity=0, argv=argv)