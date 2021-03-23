import sqlite3

connection = sqlite3.connect('audios.db')
cursor = connection.cursor()
def create_database():#Creates Database
	cursor.execute("""CREATE TABLE audios
		(id TEXT,title TEXT,thumbnail TEXT,url TEXT,description TEXT)""")
	connection.commit()
def fetchall():#Returns Database
	cursor.execute("""SELECT * FROM audios""")
	return cursor.fetchall()
def query(query):#Returns query for given query
	cursor.execute(f"SELECT * FROM audios WHERE {query}")
	return cursor.fetchall()
def addmany(audios):#Added list of tuples to Database
	cursor.executemany(f"INSERT INTO audios VALUES (?,?,?,?,?)", audios)
	connection.commit()
def display():#Displays Database to console
	audios = fetchall()
	print('id' + '\t title')
	for audio in audios:
		print(audio[0] + '\t' + audio[1])