import math
import requests
import xmltodict

import numpy as np

from app import pf_vals, pf_keys, app


def _get_user_books(user_id):
    r = requests.get(app.config['GOODREADS_URL'].format(app.config['GOODREADS_API_KEY'], user_id))
    if not r.ok:
        print(r.status_code)
        print(r.url)
    total = int(xmltodict.parse(r.text)['GoodreadsResponse']['reviews']['@total'])
    results = []
    for i in range(0, math.ceil(total / 200)):
        r = requests.get(app.config['GOODREADS_URL_PAGINATED'].format(app.config['GOODREADS_API_KEY'], user_id, i + 1))
        r_json = xmltodict.parse(r.text)
        for review in r_json['GoodreadsResponse']['reviews']['review']:
            if review['rating'] != '0':
                results += [[int(review['book']['id']['#text']), int(review['rating'])]]
    return results


def _get_book_info(book_id):
    r = requests.get(app.config['GOODREADS_BOOK_INFO_URL'].format(book_id, app.config['GOODREADS_API_KEY']))
    t = xmltodict.parse(r.text)
    fields = ['id', 'title', 'isbn', 'image_url', 'publication_year', 'publisher', 'description',
              'average_rating', 'num_pages', 'ratings_count', 'authors']
    return {key: t['GoodreadsResponse']['book'][key] for key in fields}


def recommend(user_id, n=10):
    user_books = _get_user_books(user_id)
    V = np.matrix(np.asarray(pf_vals))
    U = np.zeros(len(pf_keys))

    for (book, rating) in user_books:
        try:
            idx = pf_keys.index(book)
            U.itemset(idx, rating)
        except:
            pass

    recommendations = U * V * V.T
    top_n_recommended_book_ixs = np.where(recommendations >= np.sort(recommendations)[:, -n:].min())[1]
    top_n_recommended_book_ids = np.take(pf_keys, top_n_recommended_book_ixs)
    books = [_get_book_info(book_id) for book_id in top_n_recommended_book_ids]
    return books
