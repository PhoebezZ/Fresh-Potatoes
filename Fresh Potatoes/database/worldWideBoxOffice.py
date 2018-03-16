"""
@worldwideBoxOffice.py

@This file is to get all time worldwide box office information
@Store data into table worldwide
@Database contain 100 rows for 100 movies
"""
import requests
import re
import sqlite3
import sys
from bs4 import BeautifulSoup

def main():
	res = requests.get('http://www.boxofficemojo.com/alltime/world/')
	soup = BeautifulSoup(res.text, 'lxml')

	#Open database
	con = sqlite3.connect('boxOffice.db')
	cur = con.cursor()

	movieInfo = soup.select('div[id=body] > table > tr > td > table > tr > td > font')
	"""
	#1 Rank
	#2 Title
	#3 Studio
	#4 Worldwide
	#5 Domestic
	#6 Domestic%
	#7 Overseas
	#8 Overseas%
	#9 Year 
	"""	
	rank = []
	title = []
	studio = []
	worldwidegross = []
	domestic = []
	domestic_percent = []
	overseas = []
	overseas_percent = []
	year = []

	#First drop worldwide table
	cur.execute('DELETE FROM worldwide')

	for i in movieInfo:
		if movieInfo.index(i)%9 is 0:
			rank.append(i.get_text())
		elif movieInfo.index(i)%9 is 1:
			title.append(i.get_text())
		elif movieInfo.index(i)%9 is 2:
			studio.append(i.get_text())
		elif movieInfo.index(i)%9 is 3:
			worldwidegross.append(i.get_text())
		elif movieInfo.index(i)%9 is 4:
			domestic.append(i.get_text())
		elif movieInfo.index(i)%9 is 5:
			domestic_percent.append(i.get_text())
		elif movieInfo.index(i)%9 is 6:
			overseas.append(i.get_text())
		elif movieInfo.index(i)%9 is 7:
			overseas_percent.append(i.get_text())
		elif movieInfo.index(i)%9 is 8:
			year.append(i.get_text())
		

	for i in range(1,101):
		#print("{}\t {}\t {}\t {}\t {}\t {}\t {}\t {}\t {}\n".format(rank[i],title[i],studio[i],worldwidegross[i],domestic[i], domestic_percent[i], overseas[i], overseas_percent[i], year[i]))		
		cur.execute('INSERT INTO worldwide VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (rank[i], title[i], worldwidegross[i], domestic[i], domestic_percent[i], overseas[i], overseas_percent[i], studio[i], year[i], 0))
		con.commit()

	con.close()
	print("--------Data loading done----------")
if __name__ == "__main__":	
	main()	