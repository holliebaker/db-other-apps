# Rate My Book - A REST API

Your task is to create a database backend to work with a REST API which can be used to rate books.

There are two endpoints

- **GET**  `/books`: return a list of books in JSON format
- **POST** `/books/<id>/ratings`: allows the user to submit a rating for a book with `id`. This can be done by sending
  the JSON object specifying the number of stars. E.g.,
  ```
  { "stars": <number-of-stars> }
  ```

You can test your API using Postman: [https://www.postman.com/downloads/](https://www.postman.com/downloads/).

## Set up

```bash
# create and activate a virtual environment (don't forget the 3!)
python3 -m venv venv
. venv/bin/activate
# now install Flask
pip3 install Flask
```

## Make a RESTful API using flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "Granny Weathervax"},
    {"id": 2, "name": "Death"},
    {"id": 3, "name": "Rinsewind (Wizzard)"},
]

# retrieve all characters
@app.route('/characters', methods=['GET'])
def find_all():
    return jsonify(data)

# get one character by id
@app.route('/characters/<int:id>', methods=['GET'])
def find_by_id(book_id):
    character = next((ch for ch in data if ch["id"] == id), None)

    return jsonify(character) if character else (jsonify({"error": "Character not found"}), 404)

if __name__ == '__main__':
    app.run(debug=True)
```
## Add an SQLite3 Database

```bash
# install db-sqlite3
pip3 install db-sqlite3
```

## Make an SQLite3 database, connect to it and define the schema

```python
import sqlite3

# connect to the database
connect = sqlite3.connect('database.db')

# define the schema
# e.g., create the characters table
connect.execute(
    'CREATE TABLE IF NOT EXISTS characters (\
        id integer PRIMARY KEY,\
        name text NOT NULL\
    )'
)

# ... more tables ...

# then insert some test data
cursor = connect.cursor()
cursor.execute('INSERT INTO characters (id, name) VALUES\
    (1, "Granny Weathervax"),\
    (2, "Death"),\
    (3, "Rinsewind (Wizzard)")'
)
connect.commit()
```

## Use the database in the rest API

E.g.,
```python
# given an array of rows, each of which is an array, add the given labels to each row
def with_labels(rows, labels):
    return [dict((labels[i], value) for i, value in enumerate(row)) for row in rows]

# retrieve all characters
@app.route('/characters', methods=['GET'])
def find_all():
    # connect and get cursor
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # get all characters
    cursor.execute('SELECT id, name FROM characters')
    data = with_labels(cursor.fetchall(), ("id", "name"))

    # return characters as JSON
    return jsonify(data)

# add a new book
@app.route('/characters', methods=['POST'])
def create():
    # connect and get cursor
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # get post data as JSON
    data = request.json

    # TODO validate the data! return a 400 response if bad data sent, e.g.,
    # return jsonify({ "error": "Nome field is required." }) 400

    # insert the data
    cursor.execute('INSERT INTO characters (name) VALUES (?)', (data["name"]))
    db.commit()

    return jsonify({ "success": True }), 201 # 201 means created
```

# Your Task

- Take a look at the `app_starter.py`, which defines the two endpoints.

- In `setup-db_starter.py`, define your schema and insert some test data.

- Complete the `GET` endpoint in `app_starter.py` to return all books, along with their average rating and number of
  ratings.

- Complete the `POST` endpoint in `app_starter.py` to add a rating.

