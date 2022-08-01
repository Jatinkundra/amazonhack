import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE reviews (review TEXT, fakeDetect TEXT, sentimentDetect TEXT)')
print("Table created successfully")
conn.close()