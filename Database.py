import sqlite3
from main import results
from datetime import datetime

def createDB():
    # create a connection to the database
    conn = sqlite3.connect('verge_articles_django.db')

    # get the current date and time
    now = datetime.now()

    # format the date and time as a string
    timestamp = datetime.now().strftime("_%Y%m%d_Verge_%H%M%S")

    # create a table to store the articles
    conn.execute(f'CREATE TABLE {timestamp}_verge (id INTEGER PRIMARY KEY, name TEXT, url TEXT, author TEXT, date TEXT)')

    # insert the articles into the table
    for i, article in enumerate(results):
        conn.execute(f'INSERT INTO {timestamp}_verge (id, name, url, author, date) VALUES (?, ?, ?, ?, ?)', (i+1, article['name'], article['url'], article['author'], article['date']))

    # commit the changes and close the connection
    conn.commit()
    conn.close()
