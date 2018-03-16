#Create database to store opening this week movies
import sqlite3 as lite
import sys

con = lite.connect('movieComment.db')

with con:
	cur = con.cursor()
	#fpid: user comment, uid: user, comment: comment content
	cur.execute('CREATE TABLE opening (fpid TEXT PRIMARY KEY, uid TEXT, comment TEXT)')
	
con.close()