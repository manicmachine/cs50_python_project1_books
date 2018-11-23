import json
import os

from account import AccountManager
from book import Book as LocalBook
from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from goodReadsController import GoodReadsController
from model import User, Book, Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, static_url_path = "/static")
app.config.from_object('config') # configure environment variables

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))

# Set up account manager
accountManager = AccountManager(engine, db)

# Set up Goodreads controllers
goodReadsController = GoodReadsController(
    os.getenv("GOODREADS_KEY"),
    os.getenv("GOODREADS_SECRET"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        authRequest = {"username": request.form.get("username"),
                       "password": request.form.get("password")}

        user = accountManager.login(authRequest)
        
        if user:
            session["user"] = user
            return render_template("search.html", user = session.get("user"))
        else:
            message = "Invalid login attempt. Check your username/password and try again."
            return render_template("error.html", message=message)

    else:
        if session.get("user") is not None:
            return render_template("index.html", user = session.get("user"))
        else:
            return render_template("index.html")

@app.route("/logout", methods=["GET"])
def logout():
    accountManager.logout(session)
    
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        accountDetails = {
            "firstName": request.form.get("firstName"),
            "lastName": request.form.get("lastName"),
            "email": request.form.get("email"),
            "username": request.form.get("username"),
            "password": request.form.get("password")}
        
        if accountManager.accountExists(accountDetails['username']):
            message = "Account already exists. Try a different username."
            messageType = "error"
        elif accountManager.createAccount(accountDetails):
            message = "Account created!"
            messageType = "success"
        else:
            message = "An unknown error has occured. Contact support for assistance."
            messageType = "error"
        
        return render_template('register.html', message = message, messageType = messageType)
    else:
        return render_template('register.html')

# Return the default search page if method is GET, otherwise display results
# for the provided search criteria.
@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        search = {
            "searchBy" : request.form.get("searchBy"),
            "searchFor" : request.form.get("searchFor")}
        
        if search['searchBy'] == "isbn":
            results = db.query(Book).filter(Book.isbn.ilike('%' + search['searchFor'] + '%')).all()
        elif search['searchBy'] == "title":
            results = db.query(Book).filter(Book.title.ilike('%' + search['searchFor'] + '%')).all()
        else:
            results = db.query(Book).filter(Book.author.ilike('%' + search['searchFor'] + '%')).all()
        
        return render_template("search.html", results = results)
    else:
        return render_template("search.html")

@app.route("/book/<string:isbn>")
def book(isbn):
    
    hasReviews = False
    userReviewed = False
    book = db.query(Book).filter(Book.isbn == isbn).first()
    
    if (db.query(Review).filter(Review.book_id == isbn).count()):
        hasReviews = True
        reviews = db.query(Review).join(User).filter(Review.book_id == isbn).all()
    
    if (db.query(Review).filter(Review.book_id == isbn).filter(Review.user_id == session['user'].userId).count()):
        userReviewed = True
        userReview = db.query(Review).filter(Review.user_id == session['user'].userId).first()
        reviews.remove(userReview)
        
    reviewCounts = goodReadsController.getReviewCounts(isbn)

    localBook = LocalBook(
        isbn,
        book.title,
        book.author,
        book.year,
        reviewCounts['average_rating'],
        reviewCounts['ratings_count'])
    
    if (hasReviews and userReviewed):
        return render_template("book.html", book = localBook, reviews = reviews, userReview = userReview)
    elif (hasReviews):
        return render_template("book.html", book = localBook, reviews = reviews)
    else:
        return render_template("book.html", book = localBook)

@app.route("/api/<string:isbn>", methods=["GET"])
def queryIsbn(isbn):
    return str(isbn)

# Configure IP and Port to align with Cloud9s environment.  
if __name__ == "__main__":  
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))