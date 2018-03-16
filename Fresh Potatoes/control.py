from flask import Flask, url_for, render_template, request, redirect, make_response
from flask_mail import Mail, Message
import sqlite3
import time

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
mail = Mail(app)

#connect to boxoffice database
def con_boxoffice():
	return sqlite3.connect('/database/boxoffice.db')

#app.route('/')
#This is the homepage of freshpotatoes
#In this page, users can see following information
#	Opening this week
# 	Top boxoffice movies
#	Editor recommendation - Currently is Oscar movies
@app.route('/')
@app.route('/index')
def index():
	#This is home page
	con = sqlite3.connect('indexpagemovie.db')
	cur = con.cursor()
	tcur = con.cursor()
	Omovies = cur.execute('SELECT * FROM opening')
	Tmovies = tcur.execute('SELECT * FROM topweekend')

	return render_template('index.html', Omovies=Omovies, Tmovies=Tmovies)

#app.route('/boxoffice/domestic')
#This page shows the all time top 100 movies of domestic box office gross
#All movie informations are retrieve from boxOffice.db
@app.route('/boxoffice/domestic')
def box_office():
	#This is the box office page
	title = "Domestic - Fresh Potatoes"

	#Open database
	con = sqlite3.connect('boxoffice.db')
	cur = con.cursor()
	#Get all movie information into rows
	movies = cur.execute('SELECT * FROM domestic ORDER BY rank')

	return render_template('boxoffice_domestic.html', title=title, movies=movies)
	con.close()

#app.route('/boxoffice/worldwide')
#This page shows the all time top 100 movies of worldwide box office gross
#All movie informations are retrieve from boxOffice.db
@app.route('/boxoffice/worldwide')
def box_office_worldwide():
	#This is the box office page with worldwide record
	title = "Worldwide - Fresh Potatoes"

	con = sqlite3.connect('boxoffice.db')
	cur = con.cursor()
	movies = cur.execute('SELECT * FROM worldwide ORDER BY rank')

	return render_template('boxoffice_worldwide.html', title=title, movies=movies)

#app.route('/boxoffice/weekend')
#This page shows the all time top 100 movies of weekend box office gross
#All movie informations are retrieve from boxOffice.db
#The weekend movies will be updated once a week
@app.route('/boxoffice/weekend')
def box_office_weekend():
	#This is the box office page with worldwide record
	title = "Worldwide - Fresh Potatoes"

	con = sqlite3.connect('boxoffice.db')
	cur = con.cursor()
	movies = cur.execute('SELECT * FROM weekend ORDER BY rank')

	return render_template('boxoffice_weekend.html', title=title, movies=movies)
  
 #app.route('/about')
 #This page shows the information of developing team
 #Users can send messages to developing team in this page
@app.route('/about', methods=['POST','GET'])
def about():
	#This is the about page
	title = "About Us - Fresh Potatoes"
	if request.method == 'POST':
		# print("click send")
		msg = Message(sender="FreshPotatoes2018@gmail.com", recipients=['FreshPotatoes2018@gmail.com'])
		msg.subject = request.form['subject']
		msg.html = "This email is sent from: " + request.form['email'] + "\n Name: " + request.form['name'] + "\n Message: " + request.form['message']
		# print(msg.html)
		mail.send(msg)
		return render_template('about.html', title=title)
	else:
		return render_template('about.html', title=title)

#app.route('/ticket')
#This is the ticket generator page
#Users can generate customized movie tickets by adding information
#The ticket can be saved as pdf file or img file
@app.route('/ticket')
def ticket():
	#This is the ticket page
	title = "Ticket - Fresh Potatoes"
	return render_template('ticket.html', title=title)

#app.route('/search')
#This is the search page
#Users can search movies in the search bar
#The result will based on the movie data in movieDetail.db
@app.route('/search', methods=['POST','GET'])
def search():
	#This is the genre page
	title = "Search - Fresh Potatoes"

	if request.method == 'POST':
		movie_name = request.form['search_bar']
		movie_param = '%'+movie_name+'%'

		#Check if user input is null
		if movie_param != "%%":
			con = sqlite3.connect('movieDetail.db')
			cur = con.cursor()
			search_url = 'SELECT title, fpID FROM movie WHERE title LIKE "'+movie_param+'"'
			movies = cur.execute(search_url)
			return render_template('search.html', title=title, movies=movies, movie_name=movie_name)
		else:
			response = 'please enter a movie name'
			return render_template('search.html', title=title, response=response)
	else:
		return render_template('search.html', title=title)

#app.route('/gallery')
#In this page, user can create their movie gallery
#By adding movies into the database
#Users can view how many movies they have watched 
@app.route('/gallery')
def gallery():
	#This is the gallery page
	username = get_cookies()
	if username is None:
		return redirect(url_for('login'))
	else:
		title = "Gallery - Fresh Potatoes"
		con = sqlite3.connect('gallery.db')
		cur = con.cursor()
		selectsrc = 'SELECT * FROM gallery WHERE username="' + username + '"' + 'ORDER BY id DESC'
		movies = cur.execute(selectsrc)

		return render_template('gallery.html', title=title, username = username, movies=movies)

#app.route('/movie/<movieID>')
#This is the movie detail page
#This page contains general movie information including director, year, production etc.
#This page also has comment function that users can give function to the movie
#And also view others comments about this movie
@app.route('/movie/<movieID>', methods=['POST','GET'])
def movie_detail(movieID):
	# Open movie detail database
	movieid = movieID
	uid = get_cookies()
	if uid is None:
		uid = "Anonymous"

	if request.method == 'POST':
		
		comment = request.form['comment_text']
		commentdate = time.strftime("%Y-%m-%d")

		icon = sqlite3.connect('movieComment.db')
		icur = icon.cursor()
		#insertSQL = 'INSERT INTO opening VALUES ("'+movieid+'", '+'"'+uid+'", '+'"'+comment+'", '+'"'+commentdate+'")'
		icur.execute('INSERT INTO opening VALUES (?,?,?,?)',(movieid,uid,comment,commentdate))
		icon.commit()
		icon.close()

	con = sqlite3.connect('movieDetail.db')
	cur = con.cursor()
	# Get all movie information
	querySentence = 'SELECT * FROM movie WHERE fpID="'+movieID+'"'
	movies = cur.execute(querySentence)

	mcon = sqlite3.connect('movieComment.db')
	mcur = mcon.cursor()
	mquery = 'SELECT * FROM opening WHERE fpID="'+movieID+'"' + 'ORDER BY time DESC'
	comments = mcur.execute(mquery)

	gcon = sqlite3.connect('gallery.db')
	gcur = gcon.cursor()
	gquery = 'SELECT * FROM gallery WHERE fpID="' +movieID+'"' + ' AND username= "'+uid+'"'
	gresult = gcur.execute(gquery)
	result = gresult.fetchone()

	#Get movie posters
	src = '../static/images/posters/'+movieID+'.jpg'
	title = "Movie detail - Fresh Potatoes"
	return render_template('movie_detail.html', movies=movies, src=src, comments=comments, uid = uid, result=result)
	#return querySentence

#When user click watched movie, they will be store movie information into database
#Then will be redirect to the gallery page showing all watched movies
@app.route('/watched/<movieID>', methods=['POST','GET'])	
def movie_watched(movieID):
	if request.method == 'POST':

		moviename = request.form['movie_name']
		movieid = movieID
		uid = get_cookies() #Get username from cookies
		
		if uid is None: #No valid user log in
			return redirect(url_for('login'))
		else:
			watchdate = time.strftime("%Y-%m-%d")
			con = sqlite3.connect('gallery.db')
			cur = con.cursor()
			cur.execute('INSERT INTO gallery VALUES (?,?,?,?,null)',(uid,movieid,watchdate,moviename))
			con.commit()
			con.close()
			return redirect(url_for('gallery'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	#This is the sign up page 
	if request.method == 'POST':
		#global username
		username = request.form['username']
		password = request.form['password']
		insert = insertUser(username, password)
		if insert == 'true':
			#Insert new username into database, then set cookies
			rsp = make_response(redirect(url_for('gallery')))
			rsp.set_cookie('username', username)
			return rsp
		else:
			return render_template('signup.html', insert = insert, username = username)
	else:
		print("nothing???")
		return render_template('signup.html')

def insertUser(username,password):
	con = sqlite3.connect("users.db")
	cur = con.cursor()
	try:
		cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
		con.commit()
		print("register successfully!")
		insert = 'true'
	except:
		print("exist username")
		insert = 'false'
	con.close()
	return insert

@app.route('/login', methods=['POST', 'GET'])
def login():
	#check if has cookies
	username = get_cookies()
	if username is None:
		#no user are in cookie
		if request.method=='POST':
			print ("login_attempt")
			username = request.form['username']
			password = request.form['password']
			with sqlite3.connect("users.db") as db:
				cursor = db.cursor()
			find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
			cursor.execute(find_user, [(username), (password)])
			results = cursor.fetchall()

			if results:
				for i in results:
					print(username + "is login")
					response = make_response(redirect(url_for('login')))
					response.set_cookie('username', username)
					return response
			else: 
				return render_template('login.html', error = "true")
		else:
			return render_template('login.html')
	else:
		#Now we have a user in the cookies
		return redirect(url_for('gallery'))

@app.route('/logout')
def logout():
	username = get_cookies()
	if username is None:
		#No username
		return redirect(url_for('index'))
	else:
		#Delete cookies
		response = make_response(redirect(url_for('logout')))  
		response.set_cookie('username','',expires=0)  
		return response  

#Check if cookies hold current user
def get_cookies():
	res = request.cookies.get('username')
	return res


if __name__ == '__main__':
	#app.run()
	app.run(threaded = True)