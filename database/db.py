import sqlite3


def get_connection():
    return sqlite3.connect("data/securebank.db")


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as file:
        cursor.executescript(file.read())

    conn.commit()
    conn.close()