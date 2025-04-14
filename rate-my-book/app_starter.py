from flask import Flask, jsonify, request
import sqlite3

# given an array of rows, each of which is an array, add the given labels to each row
def with_labels(rows, labels):
    return [dict((labels[i], value) for i, value in enumerate(row)) for row in rows]


# create a flask app
app = Flask(__name__)

# retrieve all books
@app.route('/books', methods=['GET'])
def find_all():
    test_data = [

    ]
    return jsonify(test_data)

# rate a book by id
@app.route('/books/<int:book_id>/ratings', methods=['POST'])
def rate(book_id):
    # get json body and extract number of stars as an integer
    data = request.json
    stars = int(data["stars"])

    return jsonify({ "stars": stars }), 201

if __name__ == '__main__':
    app.run(debug=True)

