import sqlite3
import os
from datetime import datetime

class Creating_connection:
    connection = None

    @staticmethod
    def create_connection():
        if Creating_connection.connection == None:
            try:
                Creating_connection.connection = sqlite3.connect("../rule_engine/db.sqlite3")
                Creating_connection.connection.execute('''CREATE TABLE IF NOT EXISTS rule_book_mymodel
                    (id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    timestamp VARCHAR(100) NOT NULL,
                    data VARCHAR(100) NOT NULL);''')
            except Exception as e:
                with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "rule_validation_error"), 'a') as f:
                    log = str(datetime.today())+"\t"+"Table creation failed\n"
                    f.write(log)
            return Creating_connection.connection
        else:
            return Creating_connection.connection

