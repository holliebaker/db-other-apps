import sqlite3

# create tables and insert some data. run it once to initialise the DB
# connect to the database
connect = sqlite3.connect('database.db')

# authors table
connect.execute(
    'CREATE TABLE IF NOT EXISTS authors (\
        id integer PRIMARY KEY,\
        name text NOT NULL\
    )'
)

# genres table
connect.execute(
    'CREATE TABLE IF NOT EXISTS genres (\
        id integer PRIMARY KEY,\
        name text NOT NULL\
    )'
)

# books table
connect.execute(
    'CREATE TABLE IF NOT EXISTS books (\
        id integer PRIMARY KEY,\
        title text,\
        author integer NOT NULL,\
        FOREIGN KEY (author) REFERENCES authors (id)\
    )'
)

# linking table, since books may have multiple genres
connect.execute(
    'CREATE TABLE IF NOT EXISTS book_genres (\
        genre integer,\
        book integer,\
        PRIMARY KEY (genre, book)\
        FOREIGN KEY (book) REFERENCES books (id)\
        FOREIGN KEY (genre) REFERENCES genres (id)\
    )'
)

# rating table
connect.execute(
    'CREATE TABLE IF NOT EXISTS ratings (\
        id integer PRIMARY KEY,\
        book integer,\
        stars integer NOT NULL,\
        FOREIGN KEY (book) REFERENCES books (id)\
    )'
)

# insert some test data
cursor = connect.cursor()
cursor.execute('INSERT INTO authors\
    (id, name) VALUES (1, "Terry Pratchett"), (2, "Douglas Adams"), (3, "Lewis Caroll")')
cursor.execute('INSERT INTO genres\
    (id, name) VALUES (1, "Fantasy"), (2, "Science Fiction"), (3, "Comedy"), (4, "Childrens"), (5, "Detective"), (6, "Poetry")')
cursor.execute('INSERT INTO books (id, title, author) VALUES\
    (1, "The Truth", 1),\
    (2, "Jingo", 1),\
    (3, "Only You Can Save Mankind", 1),\
    (4, "Hitchhikers Guide To The Galaxy", 2),\
    (5, "Dirk Gently\'s Holistic Detective Agency", 2),\
    (6, "Alice In Wonderland", 3),\
    (7, "The Jabberwocky", 3)')
cursor.execute('INSERT INTO book_genres (book, genre) SELECT id, 1 FROM books')
cursor.execute('INSERT INTO book_genres (book, genre) SELECT id, 3 FROM books WHERE id <> 6')
cursor.execute('INSERT INTO book_genres (book, genre) VALUES (4, 2), (3, 4), (6, 4), (5, 5), (7, 6)')
connect.commit()


