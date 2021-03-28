import sqlite3

connection = sqlite3.connect('audios.db',check_same_thread=False)
cursor = connection.cursor()

def create_database():#Creates Database
	cursor.execute("""CREATE TABLE audios(id TEXT,title TEXT,thumbnail TEXT,url TEXT,description TEXT, playlist_id TEXT)""")
	cursor.execute("""CREATE TABLE playlist(id TEXT,title TEXT,thumbnail TEXT)""")
	connection.commit()

def fetchall_audios():#Returns Database
	cursor.execute("""SELECT * FROM audios""")
	return cursor.fetchall()

def fetchall_playlist():#Returns Database
	cursor.execute("""SELECT * FROM playlist""")
	return cursor.fetchall()

def find_by_playlist_id(playlist_id):#Returns query for given query
	cursor.execute(f"SELECT * FROM audios WHERE playlist_id = {playlist_id}")
	return cursor.fetchall()

def add(audios):#Added list of tuples to Database
	cursor.executemany(f"INSERT INTO audios VALUES (?,?,?,?,?,?)", audios)
	connection.commit()

def add_playlist(playlist):#Added list of tuples to Database
	cursor.executemany(f"INSERT INTO playlist VALUES (?,?,?)", playlist)
	connection.commit()
