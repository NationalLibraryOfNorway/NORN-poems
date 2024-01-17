from flask import Flask, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId

# Replace the URI with your actual connection string
client = MongoClient()
db = client.norn

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/browse')
def browse():
    documents = db.poems.find()  # Modify as per your collection
    documents = sorted(documents, key=lambda x: x['title'])
    
    return render_template('browse.html', documents=documents)

@app.route('/view/<doc_id>')
def view(doc_id):
    doc = db.poems.find_one({"_id": ObjectId(doc_id)})
    doc['text'] = doc['text'].replace('\n', '<br>')
    return render_template('view.html', doc=doc)


if __name__ == '__main__':
    app.run(debug=True)
