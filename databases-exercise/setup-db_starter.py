import sqlite3

# create tables and insert some data. run it once to initialise the DB
# connect to the database
connect = sqlite3.connect('database.db')

connect.execute(
    'CREATE TABLE IF NOT EXISTS ...\
    '
)

# insert some test data
cursor = connect.cursor()
cursor.execute('INSERT INTO ...')
connect.commit()

