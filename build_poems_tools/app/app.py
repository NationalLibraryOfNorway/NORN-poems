from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import OrderedDict
import os

# Replace the URI with your actual connection string
mongodb_uri = os.getenv('MONGODB_REMOTE_URI')
print(mongodb_uri)
client = MongoClient(mongodb_uri)
db = client.norn

app = Flask(__name__)

@app.route('/norn-poems/')
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/norn-poems/browse/')
@app.route('/browse')
def browse():
    documents = db.poems.find()  # Modify as per your collection
    documents = sorted(documents, key=lambda x: x['title'])
    
    return render_template('browse.html', documents=documents)

@app.route('/view/<doc_id>')
@app.route('/norn-poems/view/<doc_id>/')
def view(doc_id):
    doc = db.poems.find_one({"_id": ObjectId(doc_id)})
    doc['text'] = doc['text'].replace('\n', '<br>')
    return render_template('view.html', doc=doc)

@app.route('/books')
@app.route('/norn-poems/books/')
def books():
    documents = db.poems.find()
    # books_dct = OrderedDict()
    books_dct = {}
    for doc in documents:
        urn = doc['urn']
        if urn not in books_dct:
            books_dct[urn] = {
                'title': doc['book_title'],
                'author': doc['author'],
                'year': doc['year'],
                'urn': urn,
                'poems': []
            }
        books_dct[urn]['poems'].append(doc)
    
    for urn in books_dct:
        books_dct[urn]['poems'] = sorted(books_dct[urn]['poems'], key=lambda x: x['page_start'])
        
        # Sort books based on query parameter
    sort_by = request.args.get('sort', 'title')  # Default sort by title
    if sort_by == 'year':
        sorted_books = sorted(books_dct.items(), key=lambda x: x[1]['year'])
    elif sort_by == 'author':
        sorted_books = sorted(books_dct.items(), key=lambda x: x[1]['author'])
    else:  # Default and title sort
        sorted_books = sorted(books_dct.items(), key=lambda x: x[1]['title'])
    sorted_books = OrderedDict(sorted_books)
  
    return render_template('books.html', books=sorted_books)

@app.route('/search')
@app.route('/norn-poems/search/')
def search():
    query = {}
    dhlabid = request.args.get('dhlabid')
    title = request.args.get('title')
    author = request.args.get('author')
    year = request.args.get('year')

    if dhlabid:
        query['dhlabid'] = dhlabid
    if title:
        query['title'] = {'$regex': title, '$options': 'i'}
    if author:
        query['author'] = {'$regex': author, '$options': 'i'}
    if year:
        query['year'] = int(year)

    documents = db.poems.find(query)
    return render_template('search.html', documents=documents)

    

    
if __name__ == '__main__':
    app.run(debug=True)
