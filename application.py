import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha384

app = Flask(__name__)
engine = create_engine("postgres://qrpuxrpigcvxar:26bde601461b37b92590a274ba54a0b733036b964e43ec8a3e4698e3c7df8fd3@ec2-174-129-254-218.compute-1.amazonaws.com:5432/dadud12e7137fa")
db = scoped_session(sessionmaker(bind=engine))

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

menu = {'login':"Login",'signup':"Sign Up",'logout':"Logout"}
status = 0

@app.route('/')
@app.route('/home')
def index():
    if not session.get('user'):
        return render_template("index.html",login=menu['login'], signup=menu['signup'], status=status)
    return render_template("index.html",user=session.get('user'), logout=menu['logout'],status= not status)

@app.route('/login')
def login():
    if not session.get('user'):
        return render_template('login.html',login=menu['login'], signup=menu['signup'], status=status)
    return render_template("main.html",user=session.get('user'), logout=menu['logout'], status= not status)
    

@app.route('/reg')
def reg():
    return render_template("signup.html",login=menu['login'], signup=menu['signup'],status=status)

@app.route('/auth', methods=["POST"])
def auth():
    username = request.form.get("username")
    password = sha384(request.form.get("password").encode()).hexdigest()

    if len(username)==0 or len(password)==0:
        return render_template("login.html", message="**Please Fill the fields",
                                login=menu['login'], signup=menu['signup'],status=status)
    user = db.execute("SELECT * from users WHERE username=:username",
                        {'username':username}).fetchall()
    if not user:
        return render_template("signup.html",message="User Not Exist Please Sign Up Here",
                                login=menu['login'], signup=menu['signup'],status=status)
    if password == user[0][3]:
        session['user'] = user
        return render_template("main.html",user=session.get('user'), logout=menu['logout'],status=not status)
    else:
        return render_template('login.html',message="Invalid Used Id Or Password",login=menu['login'],
                                signup=menu['signup'],status=status)


@app.route('/register', methods=["POST"])
def signup():
    # getting data input by user in the sign up form
    name = request.form.get("name")
    username = request.form.get("username")
    password = sha384((request.form.get("password")).encode()).hexdigest()

    if len(name)==0 or len(username)==0 or len(password)==0:
        return render_template("signup.html", message="**All Fields are Mandatory",
                                login=menu['login'], signup=menu['signup'],status=status)

    #check weather user already exist or not
    user = db.execute("SELECT * FROM users WHERE username=:username",
                        {'username':username}).fetchall()
    
    if len(user)==0:   # if user doesn't exist
        db.execute("INSERT INTO users (name,username,password) VALUES (:name, :username, :password)",
                    {'name':name, 'username':username, 'password':password})
        db.commit()
        return render_template('login.html',message="signup successful",login=menu['login'],
                                 signup=menu['signup'],status=status)
    else:
        return render_template("signup.html", message="Username Already exist",login=menu['login'],
                                 signup=menu['signup'],status=status)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    return render_template("main.html",user=session.get('user'), logout=menu['logout'],status=not status)


@app.route('/search', methods=["POST"])
def search():
    user = session.get('user')
    if not user:
        return render_template("index.html",login=menu['login'], signup=menu['signup'])
    search_by = request.form.get("search_by")
    search_text = request.form.get("search_text")
    if search_by == 'isbn':
        books = db.execute("SELECT * FROM books WHERE isbn=:isbn",
                            {'isbn':search_text}).fetchall()
        if not books:
            return render_template("main.html",user=user,logout=menu['logout'],
                                    message="No book with specified ISBN Number",status=not status)
        return render_template("main.html",user=user,logout=menu['logout'],books=books,status=not status)
    
    search_text = "%"+search_text+"%"
    if search_by == 'author':
        books = db.execute("SELECT * FROM books WHERE author LIKE :search_text",
                            {'search_text':search_text}).fetchall()
        if not books:
           return render_template("main.html",user=user,logout=menu['logout'],
                                    message="No book with specified Author Name", status=not status) 
        
        return render_template("main.html",user=user,logout=menu['logout'],books=books, status=not status)

    if search_by == 'title':
        books = db.execute("SELECT * FROM books WHERE title LIKE :search_text",
                            {'search_text':search_text}).fetchall()
        
        if not books:
            return render_template("main.html",user=user,logout=menu['logout'],
                                        message="No book with specified Title", status=not status)
        
        return render_template("main.html",user=user,logout=menu['logout'],books=books, status=not status)

    return render_template("main.html",user=user, logout=menu['logout'], status=not status)

@app.route('/book/<int:book_id>')
def book(book_id):
    if not session.get('user'):
        return render_template("index.html",login=menu['login'], signup=menu['signup'],
                                    message="Please Login First", status=status)
    book = db.execute("SELECT * FROM books WHERE book_id=:book_id",
                        {'book_id':book_id}).fetchall()
    session['book'] = book
    reviews = db.execute("SELECT * FROM reviews WHERE book_id=:book_id",
                            {'book_id':book_id}).fetchall()
    return render_template("book.html",books=book, reviews = reviews,logout=menu['logout'], status=not status)

@app.route('/review', methods = ["POST"])
def review():
    review = request.form.get("review")
    name = session.get('user')[0][1]
    book_id = session.get('book')[0][0]
    if not review:
        return render_template("book.html",books = session.get('book'),logout=menu['logout'], status=not status)
    db.execute("INSERT INTO reviews (name , book_id, comment) VALUES (:name, :book_id, :comment)",
                {'name':name,'book_id':book_id, 'comment':review})
    db.commit()

    return redirect(url_for('book',book_id=book_id))

@app.route('/api/book/<int:book_id>')
def api(book_id):
    if not session.get('user'):
        return render_template("index.html",login=menu['login'], signup=menu['signup'],
                                message="To Access API Please Login First", status=status)
    book = db.execute("SELECT * FROM books WHERE book_id=:book_id",
                        {'book_id':book_id}).fetchall()
    if len(book)==0:
        return jsonify({'Error':'No Book with provided Book id'}), 422
    
    return jsonify({
                    'ISBN' : book[0][1],
                    'Title': book[0][2],
                    'Author' : book[0][3],
                    'Year' : book[0][4]
                    })
