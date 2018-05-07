import sys
import os
import unittest
import time
import traceback
import re
from collections import defaultdict, OrderedDict
import concurrent.futures

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')


sys.path.insert(0, PARENT_DIR)

TEXT_FN = os.path.join(TEST_DIR, 'data', 'text')
HTML_FN = os.path.join(TEST_DIR, 'data', 'html')
URLS_FILE = os.path.join(TEST_DIR, 'data', 'fulltext_url_list.txt')

import newspaper
from newspaper import Article, fulltext, Source, ArticleException, news_pool
from newspaper.configuration import Configuration
from newspaper.urls import get_domain


def print_test(method):

    def run(*args, **kw):
        ts = time.time()
        print('\ttesting function %r' % method.__name__)
        method(*args, **kw)
        te = time.time()
        print('\t[OK] in %r %2.2f sec' % (method.__name__, te - ts))

    return run


def mock_resource_with(filename, resource_type):

    # HTTP request by pulls text from a pre-downloaded file from Data and Text folders respectively

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

# Checks URL domains

    domain = get_domain(url)
    tld = '.'.join(domain.split('.')[-2:])
    if tld in ['co.uk', 'com.au', 'au.com']:
        end_chunks = domain.split('.')[-3:]
    else:
        end_chunks = domain.split('.')[-2:]
    base_domain = '.'.join(end_chunks)
    return base_domain


def check_url(*args, **kwargs):
    return ExhaustiveFullTextCase.check_url(*args, **kwargs)

# Skips if not in 'fulltext.txt' else extracts and checks
@unittest.skipIf('fulltext' not in sys.argv, 'Skipping fulltext tests')
class ExhaustiveFullTextCase(unittest.TestCase):
    @staticmethod
    def check_url(args):

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

    @print_test
    def test_exhaustive(self):
        with open(URLS_FILE, 'r') as f:
            urls = [d.strip() for d in f.readlines() if d.strip()]

        domain_counters = {}

        def get_filename(url):
            domain = get_base_domain(url)
            domain_counters[domain] = domain_counters.get(domain, 0) + 1
            return '{}{}'.format(domain, domain_counters[domain])

        filenames = map(get_filename, urls)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            test_results = list(executor.map(check_url, zip(urls, filenames)))

        total_pubdates_failed, total_fulltext_failed = \
            list(map(sum, zip(*test_results)))

        print('%s fulltext extractions failed out of %s' %
              (total_fulltext_failed, len(urls)))
        print('%s pubdate extractions failed out of %s' %
              (total_pubdates_failed, len(urls)))
        self.assertGreaterEqual(47, total_pubdates_failed)
        self.assertGreaterEqual(20, total_fulltext_failed)

# For nlp - Parse, MetaData, NLP
class ArticleTestCase(unittest.TestCase):
    def setup_stage(self, stage_name):
        stages = OrderedDict([
            ('initial', lambda: None),
            ('download', lambda: self.article.download(
                mock_resource_with('cnn_article', 'html'))),
            ('parse', lambda: self.article.parse()),
            ('meta', lambda: None),
            ('nlp', lambda: self.article.nlp())
        ])
        assert stage_name in stages
        for name, action in stages.items():
            if name == stage_name:
                break
            action()

#Err Fixed: Called before the first test case of this unit begins
       def setUp(self):

           self.article = Article(
               url='http://www.cnn.com/2018/03/27/weather-'
                   'march/index.html?iref=allsearch')
       @print_test
       def test_url(self):
           self.assertEqual(
               'http://www.cnn.com/2018/03/27/weather-'
               'march/index.html?iref=allsearch',
               self.article.url)

        @print_test
        def test_download_html(self):
            self.setup_stage('download')
            html = mock_resource_with('cnn_article', 'html')
            self.article.download(html)
            self.assertEqual(75406, len(self.article.html))


if __name__ == '__main__':
    argv = list(sys.argv)
    if 'fulltext' in argv:
        argv.remove('fulltext')  # remove it here, so it doesn't pass to unittest

    unittest.main(verbosity=0, argv=argv)
