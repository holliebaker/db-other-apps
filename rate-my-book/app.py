from flask import Flask, jsonify, request
import sqlite3

# given an array of rows, each of which is an array, add the given labels to each row
def with_labels(rows, labels):
    return [dict((labels[i], value) for i, value in enumerate(row)) for row in rows]


app = Flask(__name__)

# retrieve all books
@app.route('/books', methods=['GET'])
def find_all():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # get all books
    cursor.execute('SELECT books.id, title, authors.name FROM books JOIN authors ON books.author = authors.id')
    data = with_labels(cursor.fetchall(), ("id", "title", "author"))

    # for each book, get genres as an array, number of ratings and average stars
    for book in data:
        # genres
        cursor.execute('SELECT name FROM genres JOIN book_genres ON genres.id = book_genres.genre WHERE book = ?', (str(book["id"])))
        book["genres"] = [ g[0] for g in cursor.fetchall() ]

        # ratings
        cursor.execute('SELECT COUNT(id), AVG(stars) FROM ratings WHERE book = ?', (str(book["id"])))
        ratings = cursor.fetchone()
        book["number_of_ratings"] = ratings[0]
        book["average_rating"] = ratings[1]

    return jsonify(data)

# rate a book by id
@app.route('/books/<int:book_id>/ratings', methods=['POST'])
def rate(book_id):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # first verify that the book exists
    cursor.execute('SELECT 1 FROM books WHERE id = ?', (str(book_id)))
    if not cursor.fetchone():
        return jsonify({ "error": "Book does not exist." }), 404

    # get star rating out of post data
    data = request.json
    try:
        stars = data["stars"]

        if stars < 0 or stars > 5:
            return jsonify({ "error": "\"stars\" may range between 0 and 5." }), 400
    except KeyError:
        return jsonify({ "error": "POST data must include a key \"stars\"" }), 400
    except ValueError:
        return jsonify({ "error": "\"stars\" must be an integer." }), 400

    cursor.execute('INSERT INTO ratings (book, stars) VALUES (?, ?)', (str(book_id), str(stars)))
    db.commit()
    return jsonify({ "stars": stars }), 201

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)

