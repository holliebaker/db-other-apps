from flask import Flask, jsonify, request
import sqlite3

# create a flask app
app = Flask(__name__)

# lets you test the app is running
@app.route('/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def check_it_works():
    return jsonify({
      "working": True,
      "message": "It works!"
    }), 200

# array of books and ratings
books = [
  { "id": 1, "title": "Small Gods", "author": "Terry Pratchett", "total_ratings": 57, "average_rating": 4.5 },
  { "id": 2, "title": "Excel for Dummies", "author": "David H. Ringstrom", "total_ratings": 10, "average_rating": 3.1 },
  { "id": 3, "title": "The Hobbit", "author": "J. R, R, Tolkein", "total_ratings": 62, "average_rating": 4.3 },
]
id = len(books) + 1

@app.route('/api/v1/books', methods=['GET'])
def fetch_all():
  return books

def required_type(key, data, datatype):
  return key in data and isinstance(data.get(key), datatype)

def required_str(key, data):
  return required_type(key, data, str)

def required_int(key, data):
  return required_type(key, data, int)

@app.route('/api/v1/books', methods=['POST'])
def add_book():
  global books, id
  data = request.json
  if not required_str("title", data):
    return "Title is required and must be a string", 400
  if not required_str("author", data):
    return "Author is required and must be a string", 400

  new_book = {
    "id": id,
    "title": data.get("title"),
    "author": data.get("author"),
    "total_ratings": 0,
    "average_rating": 0,
  }

  books.append(new_book)
  id += 1
  return new_book, 201

def find_by_id(search_id):
  global books
  for i, book in enumerate(books):
    if book.get("id") == search_id:
      return book, i

  return None, -1

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def find_book(book_id):
  global books
  book, index = find_by_id(book_id)
  if not book:
    return f"Book with id {book_id} not found", 404

  return book, 200


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
  global books
  book, index = find_by_id(book_id)
  if not book:
    return f"Book with id {book_id} not found", 404

  books.pop(index)
  return book, 200

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
  global books
  book, index = find_by_id(book_id)
  if not book:
    return f"Book with id {book_id} not found", 404

  if not required_str("title", data):
    return "Title is required and must be a string", 400
  if not required_str("author", data):
    return "Author is required and must be a string", 400

  book["title"] = data.get("title")
  book["author"] = data.get("author")

  books[index] = book
  return book
  
@app.route('/api/v1/books/<int:book_id>/ratings', methods=['POST'])
def add_rating(book_id):
  global books
  book, index = find_by_id(book_id)
  if not book:
    return f"Book with id {book_id} not found", 404

  data = request.json
  if not required_int("rating", data):
    return "Rating is required and must be an integer", 400

  new_total = book.get("total_ratings", 0) + 1
  new_average = ((book.get("average_rating", 0) * book.get("total_ratings", 0)) + int(data.get("rating"))) / new_total

  book["total_ratings"] = new_total
  book["average_rating"] = round(new_average, 2)
  books[index] = book

  return book, 201

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
