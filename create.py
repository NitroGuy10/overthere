"""Create a new database"""
import sqlite3

connection = sqlite3.connect("overthere.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE link_pages (
        url varchar(100),
        links varchar(1000)
    );
""")

connection.commit()
connection.close()
