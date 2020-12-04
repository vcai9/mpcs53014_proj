import os


class Config(object):
    SECRET_KEY = 'secret'
    GOODREADS_API_KEY = 'XlkrscdJCPAF0m9mjtwFtA'
    GOODREADS_URL = 'https://www.goodreads.com/review/list?v=2&key={}&id={}&shelf=read'
    GOODREADS_URL_PAGINATED = 'https://www.goodreads.com/review/list?v=2&key={}&id={}&shelf=read&per_page=200&page={}'
    GOODREADS_BOOK_INFO_URL = 'https://www.goodreads.com/book/show/{}.xml?key={}'
