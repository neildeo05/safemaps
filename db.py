import sqlite3

conn = sqlite3.connect("test.db")

print("db opened successfully")

conn.execute('''
        CREATE TABLE STREETS 
        (NAME TEXT NOT NULL,
        COVID TEXT NOT NULL);
''')


print("table created successfully")
