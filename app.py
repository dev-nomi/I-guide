from this import s
from flask import Flask,render_template,request,flash,redirect,url_for,session
import pandas as pd
import pickle5 as pickle
from nltk import PorterStemmer
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/iguide_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column("id",db.Integer, primary_key=True)
  name = db.Column("name",db.String(80), unique=True, nullable=False)
  email = db.Column("email",db.String(120), unique=True, nullable=False)
  password = db.Column("password",db.String(60), nullable=False)
  feedbacks = db.relationship('Feedback', backref='user')
  students = db.relationship('Student', backref='user')

  def __repr__(self):
    return f'<User "{self.name}", "{self.email}" >'

class Feedback(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    content = db.Column("content",db.Text)
    rating = db.Column("rating",db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'<Feedback "{self.content[:20]}...">'

class Student(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    hobbies = db.Column("Hobbies",db.Text)
    goals = db.Column("Goals",db.Text)
    m_group = db.Column("M-Group",db.Text)
    m_english_marks = db.Column("M-English Marks",db.Integer)
    m_urdu_marks = db.Column("M-Urdu Marks",db.Integer)
    m_islamic_studies_marks = db.Column("M-Islamic Studies Marks",db.Integer)
    m_pak_studies_marks = db.Column("M-Pak Studies Marks",db.Integer)
    m_bio_comp_marks = db.Column("M-Bio/Comp Marks",db.Integer)
    m_physics_marks = db.Column("M-Physics Markss",db.Integer)
    m_chemistry_marks = db.Column("M-Chemistry Marks",db.Integer)
    m_mathematics_marks = db.Column("M-Mathematics Marks",db.Integer)
    i_group = db.Column("I-Group",db.Text)
    i_english_marks = db.Column("I-English Marks",db.Integer)
    i_urdu_marks = db.Column("I-Urdu Marks",db.Integer)
    i_islamic_studies_marks = db.Column("I-Islamic Studies Marks",db.Integer)
    i_pak_studies_marks = db.Column("I-Pak Studies Marks",db.Integer)
    i_math_bio_marks = db.Column("I-Math/Bio",db.Integer)
    i_physics_statistics_marks = db.Column("I-Physics/Statistics",db.Integer)
    i_comp_chem_marks = db.Column("I-Comp/Chem",db.Integer)
    program = db.Column("program",db.Text)
    feedback = db.relationship("Feedback", uselist=False, backref="student")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<StudentDetails "{self.hobbies}","{self.goals}">'

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/sign_in', methods = ['POST','GET'])
def sign_in():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email,password=password).all()
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
    try:
      user_1 = User(name=name,email=email,password=password)
      db.session.add(user_1)
      db.session.commit()
      flash('You were successfully signed up.','positive')
      return redirect(url_for('sign_in'))
    except Exception as e:
      flash("Oops! Can't be signed up.",'negative')
      return redirect(url_for('sign_up'))
  return render_template('sign_up.html')


@app.route('/new_student_details', methods = ['POST','GET'])
def new_student_details():
  if session['email'] and request.method=='POST':
    student = Student.query.order_by(Student.id.desc()).first()
    i_group_input = request.form.get('i_group')
    i_english_marks_input = request.form.get('i_english_marks')
    i_urdu_marks_input = request.form.get('i_urdu_marks')
    i_islamic_studies_marks_input = request.form.get('i_islamic_studies_marks')
    i_pak_studies_marks_input = request.form.get('i_pak_studies_marks')
    i_math_bio_marks_input = request.form.get('i_math_bio_marks')
    i_physics_statistics_marks_input = request.form.get('i_physics_statistics_marks')
    i_comp_chem_marks_input = request.form.get('i_comp_chem_marks')

    student.i_group = i_group_input
    student.i_english_marks = i_english_marks_input
    student.i_urdu_marks = i_urdu_marks_input 
    student.i_islamic_studies_marks = i_islamic_studies_marks_input
    student.i_pak_studies_marks = i_pak_studies_marks_input
    student.i_math_bio_marks =i_math_bio_marks_input
    student.i_physics_statistics_marks = i_physics_statistics_marks_input
    student.i_comp_chem_marks = i_comp_chem_marks_input

    db.session.commit()
    flash('You were successfully added student details.','positive')
    return redirect(url_for('show_student'))
  elif request.method == 'GET':
    return render_template('student/add.html')
  else:
    flash('Access denied.','negative')
    return redirect(url_for('home'))

@app.route('/sign_out')
def sign_out():
  session['email'] = None
  flash('You were successfully signed out.','positive')
  return redirect(url_for('home'))

@app.route('/feedback', methods = ['POST','GET'])
def feedback():
  if session['email'] and request.method=='POST':
    user = User.query.filter_by(email = session['email']).all()
    student = Student.query.order_by(Student.id.desc()).first()
    comment_input = request.form.get('comment')
    rating_input = request.form.get('rating')
    feedback = Feedback(
      content=comment_input,
      rating=rating_input,
      user=user[0],
      student=student
    )
    db.session.add(feedback)
    db.session.commit()
    flash('You were successfully added feedback.','positive')
    return redirect(url_for('feedbacks'))
  else:
    return render_template('feedback/add.html')

@app.route('/feedbacks')
def feedbacks():
  feedbacks = Feedback.query.all()
  return render_template('feedback/index.html', feedbacks=feedbacks )

@app.route('/student_info',methods = ['POST','GET'])
def student_info():
  if request.method == 'POST':
    user = User.query.filter_by(email = session['email']).all()
    hobbies_input = request.form.get('hobbies')
    goals_input = request.form.get('goals')

    student = Student(
      hobbies=hobbies_input,
      goals=goals_input,
      user=user[0],
    )
    db.session.add(student)
    db.session.commit()
    return '', 204

@app.route('/student_matric_marks',methods = ['POST','GET'])
def student_matric_marks():
  if request.method == 'POST':
    student = Student.query.order_by(Student.id.desc()).first()
    m_group_input = request.form.get('m_group')
    m_english_marks_input = request.form.get('m_english_marks')
    m_urdu_marks_input = request.form.get('m_urdu_marks')
    m_islamic_studies_marks_input = request.form.get('m_islamic_studies_marks')
    m_pak_studies_marks_input = request.form.get('m_pak_studies_marks')
    m_bio_comp_marks_input = request.form.get('m_bio_comp_marks')
    m_physics_marks_input = request.form.get('m_physics_marks')
    m_chemistry_marks_input = request.form.get('m_chemistry_marks')
    m_mathematics_marks_input = request.form.get('m_mathematics_marks')

    student.m_group = m_group_input
    student.m_english_marks = m_english_marks_input
    student.m_urdu_marks =  m_urdu_marks_input
    student.m_islamic_studies_marks =  m_islamic_studies_marks_input
    student.m_pak_studies_marks = m_pak_studies_marks_input 
    student.m_bio_comp_marks = m_bio_comp_marks_input
    student.m_physics_marks = m_physics_marks_input
    student.m_chemistry_marks =  m_chemistry_marks_input
    student.m_mathematics_marks =  m_mathematics_marks_input

    db.session.commit()
    return '', 204

@app.route('/show_student')
def show_student():
  student = Student.query.order_by(Student.id.desc()).first()
  return render_template('student/show.html', student = student)

@app.route('/predict')
def predict():
  student = Student.query.order_by(Student.id.desc()).first()
  
  user_input = pd.DataFrame({
    'Hobbies': student.hobbies,
    'Goals': student.goals,
    "M-Group": student.m_group,
    "M-English Marks":student.m_english_marks,
    "M-Urdu Marks":student.m_urdu_marks,
    "M-Islamic Studies Marks":student.m_islamic_studies_marks,
    "M-Pak Studies Marks":student.m_pak_studies_marks,
    "M-Bio/Comp Marks":student.m_bio_comp_marks,
    "M-Physics Marks":student.m_physics_marks,
    "M-Chemistry Marks":student.m_chemistry_marks,
    "M-Mathematics Marks":student.m_mathematics_marks,
    "I-Group": student.i_group,
    "I-English Marks":student.i_english_marks,
    "I-Urdu Marks":student.i_urdu_marks,
    "I-Pak Studies Marks":student.i_pak_studies_marks,
    "I-Islamic Studies Marks":student.i_islamic_studies_marks,
    "I-Math/Bio":student.i_math_bio_marks,
    "I-Physics/Statistics":student.i_physics_statistics_marks,
    "I-Comp/Chem":student.i_comp_chem_marks
  },index=[0])


  m_group_pkl_file = open('./models/m_group_label_encoder.pkl', 'rb')
  m_group_label_encoder = pickle.load(m_group_pkl_file) 
  m_group_pkl_file.close()

  i_group_pkl_file = open('./models/i_group_label_encoder.pkl', 'rb')
  i_group_label_encoder = pickle.load(i_group_pkl_file) 
  i_group_pkl_file.close()


  #Transform Input (Categorical) Attributes of Unseen Data into Numerical Representation
  unseen_data_features = user_input.copy()
  unseen_data_features["M-Group"] = m_group_label_encoder.transform(user_input['M-Group'])
  unseen_data_features["I-Group"] = i_group_label_encoder.transform(user_input['I-Group'])

  unseen_data_features['Hobbies'] = unseen_data_features['Hobbies'].str.replace("[^a-zA-Z#]", " ", regex=True)
  unseen_data_features['Goals'] = unseen_data_features['Goals'].str.replace("[^a-zA-Z#]", " ", regex=True)

  unseen_data_features['Hobbies'] = unseen_data_features['Hobbies'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>5]))
  unseen_data_features['Goals'] = unseen_data_features['Goals'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))

  tokenized_hobbies = unseen_data_features['Hobbies'].apply(lambda x: x.split())
  tokenized_goals = unseen_data_features['Goals'].apply(lambda x: x.split())

  ps = PorterStemmer()
  tokenized_hobbies = tokenized_hobbies.apply(lambda x: [ps.stem(i) for i in x])
  tokenized_goals = tokenized_goals.apply(lambda x: [ps.stem(i) for i in x])

  unseen_data_features['Hobbies'] = ' '.join(tokenized_hobbies[0])
  unseen_data_features['Goals'] = ' '.join(tokenized_goals[0])

  hobbies = unseen_data_features['Hobbies']
  count_vectorizer_hobbies_pkl_file = open('./models/count_vectorizer_hobbies_unigram_to_trigram.pkl', 'rb')
  count_vectorizer_hobbies = pickle.load(count_vectorizer_hobbies_pkl_file) 
  count_vectorizer_hobbies_pkl_file.close()
  # Transform the Input Text using Count Vectorizer
  transform_features = count_vectorizer_hobbies.transform(hobbies)

  # Get the name of Features (Feature  Set)
  feature_set = count_vectorizer_hobbies.get_feature_names_out()

  # Convert Transformed features into Array and Create a Dataframe
  hobbies_input_features = pd.DataFrame(transform_features.toarray(), columns = feature_set)


  goals = unseen_data_features['Goals']
  count_vectorizer_goals_pkl_file = open('./models/count_vectorizer_goals_unigram_to_trigram.pkl', 'rb')
  count_vectorizer_goals = pickle.load(count_vectorizer_goals_pkl_file) 
  count_vectorizer_goals_pkl_file.close()

  # Transform the Input Text using Count Vectorizer
  transform_features = count_vectorizer_goals.transform(goals)

  # Get the name of Features (Feature  Set)
  feature_set = count_vectorizer_goals.get_feature_names_out()

  # Convert Transformed features into Array and Create a Dataframe
  goals_input_features = pd.DataFrame(transform_features.toarray(), columns = feature_set)
  unseen_data_features.drop(['Hobbies', 'Goals'], axis=1, inplace=True)
  unseen_data_features = pd.concat([unseen_data_features, hobbies_input_features], axis=1, join='inner')
  unseen_data_features = pd.concat([unseen_data_features, goals_input_features], axis=1, join='inner')

  model = pickle.load(open('./models/gnb_trained_model.pkl', 'rb'))
  predicted_program = model.predict(unseen_data_features)
  student = Student.query.order_by(Student.id.desc()).first()

  if(predicted_program == 0): 
    prediction = "BS Chemical Engineering"
  elif(predicted_program == 1):
    prediction = "BS Computer Engineering"
  elif(predicted_program == 2):
    prediction = "BS Computer Sciences"
  elif(predicted_program == 3):
    prediction = "BS Electrical Engineering"
  elif(predicted_program == 4):
    prediction = "BS Software Engineering"

  student.program = prediction
  db.session.commit()
  return render_template('prediction.html',prediction=prediction)

@app.route('/predictions',methods = ['POST','GET'])
def predictions():
  user = User.query.filter_by(email = session['email']).all()
  predictions = user[0].students
  return render_template('prediction/index.html',predictions=predictions)