"""
OMDbRequest.py
User input movie name and year
The OMDB database will return the detail of movie

$ sudo pip3 install requests
"""
import requests
import re
import sqlite3 as lite
import sys

def getMovieInfo(movie_name, movie_year):

	#To get movie data, need apikey: a5395c65
	url = 'http://img.omdbapi.com/?apikey=a5395c65&t={}&y={}'.format(movie_name, movie_year)

	res = requests.post(url)
	resJson = res.json()
	
	con = lite.connect('movieDetail.db')
	cur = con.cursor()

	try:	
		Title = resJson['Title']
		Year = resJson['Year']
		Production = resJson['Production']
		Director = resJson['Director']
		imdbID = resJson['imdbID']
		MetaScore = resJson['Metascore']
		ImdbRating = resJson['imdbRating']
		RottenRating = resJson['Ratings'][1]['Value']
		Plot = resJson['Plot']
		length = resJson['Runtime']
		genre = resJson['Genre']
		country = resJson['Country']
		rated = resJson['Rated']
		language = resJson['Language']

		#Print out the information of movie, for test
		#print("\n\n")
		#print("Title: {}\nYear: {}\nProduction: {}\nDirector: {}\nimdbID: {}\nScore: Rotten Tomatoes:{}, MetaScore:{}, IMDB:{}\nPlot: {}".format(Title, Year, Production, Director, imdbID, RottenRating, MetaScore, ImdbRating, Plot))
		#print("\n\n")

		fpID = input("fpID: ")
		if int(fpID) < 10:
			fpID = "fp00" + fpID
		elif int(fpID) > 10 and int(fpID) < 100:
			fpID = "fp0" + fpID
		else:
			fpID = "fp" + fpID

		#Insert into table movie
		cur.execute('INSERT INTO movie VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (fpID, Title, Year, Production, Director, imdbID, MetaScore, ImdbRating, RottenRating, Plot, length, genre, country, rated, language))
		con.commit()

	except:
		print("Error occurs")

	#Close database
	con.close()
	print("----------Inserting done----------")

def main():

	#用户端输入 电影名/年份
	name = input("enter a  movie name: ")
	year = input("enter the year of the movie: ")
	getMovieInfo(name, year)


if __name__ == "__main__":
	main()
