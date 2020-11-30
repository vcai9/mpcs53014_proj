import math
import requests
import xmltodict

import numpy as np

from app import pf_vals, pf_keys


KEY = 'XlkrscdJCPAF0m9mjtwFtA'


def _get_user_books(user_id):
    r = requests.get(
        'https://www.goodreads.com/review/list?v=2&key={}&id={}&shelf=read'.format(KEY, user_id))
    if not r.ok:
        print(r.status_code)
        print(r.url)
    total = int(xmltodict.parse(r.text)['GoodreadsResponse']['reviews']['@total'])
    results = []
    for i in range(0, math.ceil(total / 200)):
        r = requests.get(
            'https://www.goodreads.com/review/list?v=2&key={}&id={}&shelf=read&per_page=200&page={}'.format(KEY,
                user_id, i + 1))
        r_json = xmltodict.parse(r.text)
        for review in r_json['GoodreadsResponse']['reviews']['review']:
            if review['rating'] != '0':
                results += [[int(review['book']['id']['#text']), int(review['rating'])]]
    return results


def _get_book_info(book_id):
    r = requests.get('https://www.goodreads.com/book/show/{}.xml?key={}'.format(book_id, KEY))
    t = xmltodict.parse(r.text)
    fields = ['id', 'title', 'isbn', 'image_url', 'publication_year', 'publisher', 'description',
              'average_rating', 'num_pages', 'ratings_count', 'authors']
    return {key: t['GoodreadsResponse']['book'][key] for key in fields}


def recommend(user_id, n=10):
    user_books = _get_user_books(user_id)
    Vt = np.matrix(np.asarray(pf_vals))
    full_u = np.zeros(len(pf_keys))

    def set_rating(key, val):
        try:
            idx = pf_keys.index(key)
            full_u.itemset(idx, val)
        except:
            pass

    for (book, rating) in user_books:
        set_rating(book, rating)

    recommendations = full_u * Vt * Vt.T
    top_n_recommended_book_ixs = np.where(recommendations >= np.sort(recommendations)[:, -n:].min())[1]
    top_n_recommended_book_ids = np.take(pf_keys, top_n_recommended_book_ixs)
    books = [_get_book_info(book_id) for book_id in top_n_recommended_book_ids]
    return books
