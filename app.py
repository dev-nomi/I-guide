from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/sign_in', methods = ['POST','GET'])
def sign_in():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users where password=? and email=?',(password,email,)).fetchall()
    conn.close()
    if user:
      session['email'] = email
      flash('You were successfully signed in.','positive')
      return redirect(url_for('new_student_details'))
    else:
      flash('Invalid credentials','negative')
      return render_template('sign_in.html')
  return render_template('sign_in.html')

@app.route('/sign_up', methods = ['POST','GET'])
def sign_up():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    conn = get_db_connection()
    user = conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password))
    conn.commit()
    conn.close()
    flash('You were successfully signed up.','positive')
    return redirect(url_for('sign_in'))
  return render_template('sign_up.html')


@app.route('/new_student_details')
def new_student_details():
  if session['email']:
    return render_template('new_student_details.html')
  else:
    flash('Access denied.','negative')
    return render_template('home.html')

@app.route('/sign_out')
def sign_out():
  session['email'] = None
  flash('You were successfully signed out.','positive')
  return render_template('home.html')
