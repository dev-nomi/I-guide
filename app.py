from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3
import pandas as pd
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


@app.route('/new_student_details', methods = ['POST','GET'])
def new_student_details():
  if session['email']:
    hobbies_input = request.form.get('hobbies')
    goals_input = request.form.get('goals')
    m_group_input = request.form.get('m_group')
    m_english_marks_input = request.form.get('m_english_marks')
    m_urdu_marks_input = request.form.get('m_urdu_marks')
    m_islamic_studies_marks_input = request.form.get('m_islamic_studies_marks')
    m_pak_studies_marks_input = request.form.get('m_pak_studies_marks')
    m_bio_comp_marks_input = request.form.get('m_bio_comp_marks')
    m_physics_marks_input = request.form.get('m_physics_marks')
    m_chemistry_marks_input = request.form.get('m_chemistry_marks')
    m_mathematics_marks_input = request.form.get('m_mathematics_marks')
    i_group_input = request.form.get('i_group')
    i_english_marks_input = request.form.get('i_english_marks')
    i_urdu_marks_input = request.form.get('i_urdu_marks')
    i_islamic_studies_marks_input = request.form.get('i_islamic_studies_marks')
    i_pak_studies_marks_input = request.form.get('i_pak_studies_marks')
    i_math_bio_marks_input = request.form.get('i_math_bio_marks')
    i_physics_statistics_marks_input = request.form.get('i_physics_statistics_marks')
    i_comp_chem_marks_input = request.form.get('i_comp_chem_marks')

    user_input = pd.DataFrame({ 
      'Hobbies': [hobbies_input],
      'Goals': [goals_input],
      "M-Group": [m_group_input],
      "M-English Marks":[m_english_marks_input],
      "M-Urdu Marks":[m_urdu_marks_input],
      "M-Islamic Studies Marks":[m_islamic_studies_marks_input],
      "M-Pak Studies Marks":[m_pak_studies_marks_input],
      "M-Bio/Comp Marks":[m_bio_comp_marks_input],
      "M-Physics Marks":[m_physics_marks_input],
      "M-Chemistry Marks":[m_chemistry_marks_input],
      "M-Mathematics Marks":[m_mathematics_marks_input],
      "I-Group": [i_group_input],
      "I-English Marks":[i_english_marks_input],
      "I-Urdu Marks":[i_urdu_marks_input],
      "I-Pak Studies Marks":[i_pak_studies_marks_input],
      "I-Islamic Studies Marks":[i_islamic_studies_marks_input],
      "I-Math/Bio":[i_math_bio_marks_input],
      "I-Physics/Statistics":[i_physics_statistics_marks_input],
      "I-Comp/Chem":[i_comp_chem_marks_input],
    })

    # Transform Input (Categorical) Attributes of Unseen Data into Numerical Representation
    unseen_data_features = user_input.copy()
    unseen_data_features["M-Group"] = m_group_label_encoder.transform(user_input['M-Group'])
    unseen_data_features["I-Group"] = i_group_label_encoder.transform(user_input['I-Group'])
    
    return render_template('new_student_details.html')
  else:
    flash('Access denied.','negative')
    return render_template('home.html')

@app.route('/sign_out')
def sign_out():
  session['email'] = None
  flash('You were successfully signed out.','positive')
  return render_template('home.html')
