import flask
from flask import Flask, send_from_directory, jsonify
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint
import request_api
from utils import api_client
from utils.api_client import sort
from utils.config_read import configReader

app = Flask(__name__)
app.debug = True

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Books Rest Api'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(request_api.get_blueprint())
config = configReader()
app.secret_key = config['app']['secret_key']



app.config['MONGO_URI'] = config['database']['db_endpoint']
mongodb_client = PyMongo(app)
db = mongodb_client.db



@app.route('/books', methods=['GET'])
def get_books():
    response_get_all_books, status_code = api_client.get_all_books()

    return response_get_all_books

@app.route('/books/id/<book_id>', methods=['GET'])
def get_books_by_id(book_id):
    response_get_books_by_id, status_code = api_client.get_book_by_id(book_id)

    return response_get_books_by_id

@app.route('/books/date/<published_date>', methods=['GET'])
def get_books_by_date(published_date):
    response_get_books_by_date, status_code = api_client.get_all_books()

    if status_code !=200:
        return jsonify({'message': 'Published date not found'})

    books = []
    data =[]

    for item in response_get_books_by_date['items']:
        if item['volumeInfo']['publishedDate'] != None:
            data.append(item)

    for book in data:
        published =  book['volumeInfo']['publishedDate']
        if str(published_date) in published:
            books.append(book)

    return jsonify({'books': books})

@app.route('/books/date/sort_by_latest', methods=['GET'])
def sort_books_by_newest():
    response_sort_books_by_latest, status_code = api_client.get_all_books()

    books = []

    for item in response_sort_books_by_latest['items']:
        if item['volumeInfo']['publishedDate'] != None:
            books.append(item)
    books.sort(reverse=True, key=sort)

    return jsonify({'books': books})

@app.route('/books/date/sort_by_eldest', methods=['GET'])
def sort_books_by_eldest():
    response_sort_books_by_eldest, status_code = api_client.get_all_books()

    books = []

    for item in response_sort_books_by_eldest['items']:
        if item['volumeInfo']['publishedDate'] != None:
            books.append(item)
    books.sort(reverse=False, key=sort)

    return jsonify({'books': books})

@app.route('/books/author/<author_name>', methods=['GET'])
def get_books_by_author(author_name):
    response_get_books_by_author,status_code = api_client.get_book_by_author(author_name)

    if status_code != 200:
        return jsonify({'message': 'Author not found'})

    return response_get_books_by_author, status_code



@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hey, it is Rest API in Flask'})



if __name__ == "__main__":
    app.run(debug=True)