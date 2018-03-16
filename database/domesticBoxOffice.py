"""
@domesticBoxOffice.py

@This file is to get all time domestic gross from boxofficemojo.com
@The movie data will be stored into table domestic
@Database contains 100 rows for 100 movies
"""
import requests
import re
import sqlite3
import sys
from bs4 import BeautifulSoup

def main():
	#Get the url address of boxofficemojo website domestic 
	res = requests.get('http://www.boxofficemojo.com/alltime/domestic.htm')
	soup = BeautifulSoup(res.text, 'lxml')

	con = sqlite3.connect('boxOffice.db')
	cur = con.cursor()

	#Get movie information by split other website information
	movieInfo = soup.select('div[id=body] > table > tr > td > center > table > tr > td > table > tr > td > font')

	"""
	#1 Rank
	#2 Title
	#3 Studio
	#4 Lifetime gross
	#5 Year
	"""	
	title = []
	studio = []
	domesticGross = []
	year = []
	rank = []
	#For each time getting movie data, we first delete all rows in table
	cur.execute('DELETE FROM domestic')

	#Append movie detials into created array
	for i in movieInfo:
		if movieInfo.index(i)%5 is 0:
			rank.append(i.get_text())
		elif movieInfo.index(i)%5 is 1:
			title.append(i.get_text())
		elif movieInfo.index(i)%5 is 2:
			studio.append(i.get_text())
		elif movieInfo.index(i)%5 is 3:
			domesticGross.append(i.get_text())
		elif movieInfo.index(i)%5 is 4:
			year.append(i.get_text())

	#Iterate each movie item
	for i in range(1,101):
		#print("{}\t {}\t {}\t {}\t {}\n".format(rank[i],title[i],studio[i],domesticGross[i],year[i]))		
		cur.execute('INSERT INTO domestic VALUES (null, ?, ?, ?, ?, ?, ?)', (rank[i], title[i], domesticGross[i], studio[i], year[i], 0))
		con.commit()

	print("------------Data query done------------")
	con.close()	

if __name__ == "__main__":	
	main()	