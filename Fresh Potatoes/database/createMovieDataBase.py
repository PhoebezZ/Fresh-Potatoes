import sqlite3 as lite
import sys

#Create movie detail database
con = lite.connect('movieDetail.db')

with con:
	cur = con.cursor()
	#Create table movie storing movie information
	cur.execute("CREATE TABLE movie (id INTEGER PRIMARY KEY AUTOINCREMENT, fpID TEXT UNIQUE, title TEXT UNIQUE, year INTEGER, production TEXT, director TEXT, imdbID TEXT, metascore TEXT, imdbrating TEXT, rottenrating TEXT, plot TEXT, length TEXT, genre TEXT, country TEXT, rated TEXT, language TEXT)")

con.close()