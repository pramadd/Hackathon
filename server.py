from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5
import re

app = Flask(__name__)
mysql = MySQLConnector(app,'reddit')
app.secret_key = "ThisIsSecret!"
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session and 'username' in session:
        return redirect('/')
# -- subreddit posts --
    subpost_query="SELECT posts.text, posts.created_at, users.username, subreddits.url FROM posts JOIN users ON posts.user_id=users.id JOIN subreddits ON posts.subreddit_id=subreddit_id LIMIT 0,50"
    subposts=mysql.query_db(subpost_query)

    return render_template('index.html', all_subposts=subposts)

@app.route('/create', methods=['POST'])
def create_user():
    if len(request.form['username'])<1:
        flash(u"Username cannot be blank!","registration")
    if len(request.form['password'])<8:
        flash(u"Password must be at least 8 characters long","registration")
    if request.form['confirm_password']==request.form['password']:
        flash(u"Password does not match","registration")
    else:
        username= request.form['username']
        password= md5.new(request.form['password']).hexdigest()
        insert_query="INSERT INTO users (username,password) VALUES (:username, :password)"
        query_data={'username':username, 'password':password}
        mysql.query_db(insert_query,query_data)
        return redirect('/')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    username=request.form['username']
    password = md5.new(request.form['password']).hexdigest()
    user_query= "SELECT * FROM users WHERE users.username= :username AND users.password=:password"
    query_data={'username':username, 'password':password}
    user= mysql.query_db(user_query,query_data)
    if user:
        session['user_id']=int(user[0]['id'])
        session['username']=int(user[0]['id'])
        return redirect('/')
    else:
        flash(u"User email or password invalid","login")
    return redirect('/')

# @app.route('/add_subred', methods=['post'])
# def add_subred():
#         subreddit = request.form['subreddit']
#         insert_query_add_sub= "INSERT INTO subreddits (user_id, subreddit_id) VALUES (:user_id, :subreddit_id,)"
#         query_data = {
#             "subreddit": request.form['subreddit'],
#             "users_id": session['id']
#         }
#         mysql.query_db(insert_query_comment, query_data)
#             return render_template('add_sub.html')


#@app.route('')
app.run(debug=True)