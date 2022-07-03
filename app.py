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
   
  def __repr__(self):
    return f'<User "{self.name}", "{self.email}" >'

class Feedback(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    content = db.Column("content",db.Text)
    rating = db.Column("rating",db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Feedback "{self.content[:20]}...">'

student_details = {
}

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
    i_group_input = request.form.get('i_group')
    i_english_marks_input = request.form.get('i_english_marks')
    i_urdu_marks_input = request.form.get('i_urdu_marks')
    i_islamic_studies_marks_input = request.form.get('i_islamic_studies_marks')
    i_pak_studies_marks_input = request.form.get('i_pak_studies_marks')
    i_math_bio_marks_input = request.form.get('i_math_bio_marks')
    i_physics_statistics_marks_input = request.form.get('i_physics_statistics_marks')
    i_comp_chem_marks_input = request.form.get('i_comp_chem_marks')

    student_details['I-Group'] = i_group_input
    student_details["I-English Marks"] = i_english_marks_input
    student_details["I-Urdu Marks"] = i_urdu_marks_input
    student_details["I-Islamic Studies Marks"] = i_islamic_studies_marks_input
    student_details["I-Pak Studies Marks"] = i_pak_studies_marks_input
    student_details["I-Math/Bio"] = i_math_bio_marks_input
    student_details["I-Physics/Statistics"]=i_physics_statistics_marks_input
    student_details["I-Comp/Chem"]= i_comp_chem_marks_input

    session['student_details'] = student_details

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
    comment_input = request.form.get('comment')
    rating_input = request.form.get('rating')
    feedback = Feedback(content=comment_input,rating=rating_input,user=user[0])
    db.session.add(feedback)
    db.session.commit()
    flash('You were successfully added feedback.','positive')
    return redirect(url_for('home'))
  else:
    return render_template('feedback/add.html')

@app.route('/feedbacks')
def feedbacks():
  feedbacks = Feedback.query.all()
  return render_template('feedback/index.html', feedbacks=feedbacks )

@app.route('/student_info',methods = ['POST','GET'])
def student_info():
  if request.method == 'POST':
    hobbies_input = request.form.get('hobbies')
    goals_input = request.form.get('goals')

    student_details['Hobbies'] = hobbies_input
    student_details['Goals'] = goals_input
    session['student_details'] = student_details
    return '', 204

@app.route('/student_matric_marks',methods = ['POST','GET'])
def student_matric_marks():
  if request.method == 'POST':
    m_group_input = request.form.get('m_group')
    m_english_marks_input = request.form.get('m_english_marks')
    m_urdu_marks_input = request.form.get('m_urdu_marks')
    m_islamic_studies_marks_input = request.form.get('m_islamic_studies_marks')
    m_pak_studies_marks_input = request.form.get('m_pak_studies_marks')
    m_bio_comp_marks_input = request.form.get('m_bio_comp_marks')
    m_physics_marks_input = request.form.get('m_physics_marks')
    m_chemistry_marks_input = request.form.get('m_chemistry_marks')
    m_mathematics_marks_input = request.form.get('m_mathematics_marks')

    student_details['M-Group'] = m_group_input
    student_details["M-English Marks"] = m_english_marks_input
    student_details["M-Urdu Marks"] = m_urdu_marks_input
    student_details["M-Islamic Studies Marks"] = m_islamic_studies_marks_input
    student_details["M-Pak Studies Marks"] = m_pak_studies_marks_input
    student_details["M-Bio/Comp Marks"]= m_bio_comp_marks_input
    student_details["M-Physics Marks"]= m_physics_marks_input
    student_details["M-Chemistry Marks"]= m_chemistry_marks_input
    student_details["M-Mathematics Marks"]= m_mathematics_marks_input
    session['student_details'] = student_details
    return '', 204

@app.route('/show_student')
def show_student():
  student = session['student_details']
  return render_template('student/show.html', student = student)

@app.route('/predict')
def predict():
  user_input = pd.DataFrame(student_details, index=[0])

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


  return render_template('prediction.html',prediction=prediction)
