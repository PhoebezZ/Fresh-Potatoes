import requests
import re
import sqlite3
import sys
from bs4 import BeautifulSoup

def main():
	week_number = input("Enter the week number: ")
	#year parameter
	year = 2018
	#week parameter
	if int(week_number) < 10:
		week_number = '0' + week_number

	url = 'http://www.boxofficemojo.com/weekend/chart/?yr={}&wknd={}&p=.htm'.format(year, week_number)
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'lxml')

	#Open database
	con = sqlite3.connect('boxOffice.db')
	cur = con.cursor()

	movie_info = soup.select('div[id=body] > table > tr > td > table > tr > td > font')

	title = []
	weekendgross = []
	totalgross = []
	studio = []

	#First drop worldwide table
	cur.execute('DELETE FROM worldwide')

	for i in movie_info:
		if movie_info.index(i) % 12 == 2: #title
			title.append(i.get_text())
		if movie_info.index(i) % 12 == 3: #studio
			studio.append(i.get_text())
		if movie_info.index(i) % 12 == 4: #weekend gross
 			weekendgross.append(i.get_text())
		if movie_info.index(i) % 12 == 9: #total gross
			totalgross.append(i.get_text())

	for i in range(1,21):
		#print("{}\t {}\t {}\t {}\t {}\n".format(i, title[i], studio[i], weekendgross[i], totalgross[i]))
		cur.execute('INSERT INTO weekend VALUES (null, ?, ?, ?, ?, ?, ?)', (i, title[i], weekendgross[i], totalgross[i], studio[i], 0))
		con.commit()

	con.close()
	print("--------Data loading done----------")

if __name__ == "__main__":	
	main()	