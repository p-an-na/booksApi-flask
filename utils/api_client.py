import logging
import requests

from utils.config_read import configReader


def get_api_endpoint():
    config = configReader()
    url = config['url']['api_endpoint']
    return url

def get_all_books():
    params = {'q': 'books'}
    response = requests.get(get_api_endpoint(), params = params)
    logging.debug('Response get all books:', response.text, 'Response status code:', response.status_code)
    status_code = response.status_code
    response = response.json()
    return response, status_code

def get_book_by_date(published_date):
    params = {'q': 'books'}
    response = requests.get(get_api_endpoint(), params = params)
    logging.debug('Response get books by published date:', response.text, 'Response status code:', response.status_code)
    status_code = response.status_code
    response = response.json()


    return response, status_code


def get_book_by_author(author_name):
    params= {'q' : 'books?authors=' + author_name}

    response = requests.get(get_api_endpoint(), params=params)
    logging.debug('Response get books by author:', response.text, 'Response status code:', response.status_code)
    status_code = response.status_code
    response = response.json()

    return response, status_code

def get_book_by_id(book_id):
    response = requests.get(get_api_endpoint() + '/' + book_id)
    logging.debug('Response get books by id:', response.text, 'Response status code:', response.status_code)
    status_code = response.status_code
    response = response.json()
    return response, status_code

def sort(e):
  return e['volumeInfo']['publishedDate']


def to_bson(self):
    data = self.dict(by_alias=True, exclude_none=True)
    if data["_id"] is None:
        data.pop("_id")
    return data