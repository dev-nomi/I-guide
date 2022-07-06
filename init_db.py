from app import db, User, Feedback,University

db.drop_all()
db.create_all()

user1 = User(name="noman", email="noman@gmail.com", password="elevenstar11")
user2 = User(name="noman khalid", email="noman@khalid.com", password="elevenstar11")

feedback1 = Feedback(content='First feedback', rating=3, user=user1)
feedback2 = Feedback(content='Second feedback', rating=1, user=user1)

university1 = University(
  name="COMSATS University LHR", 
  course_offered="BS Computer Sciences", 
  fee=99500
)

university2 = University(
  name="COMSATS University LHR", 
  course_offered="BS Software Engineering", 
  fee=99500
)

university3 = University(
  name="COMSATS University LHR", 
  course_offered="BS Electrical Engineering", 
  fee=110000
)

university4 = University(
  name="COMSATS University LHR", 
  course_offered="BS Computer Engineering", 
  fee=110000
)

university5 = University(
  name="COMSATS University LHR", 
  course_offered="BS Chemical Engineering", 
  fee=110000
)

university6 = University(
  name="University  of the punjab", 
  course_offered="BS Computer Sciences", 
  fee=48650
)

university7 = University(
  name="University  of the punjab", 
  course_offered="BS Software Engineering", 
  fee=48650
)

university8 = University(
  name="University  of the punjab", 
  course_offered="BS Chemical Engineering", 
  fee=27650
)


db.session.add_all([user1,user2])
db.session.add_all([feedback1, feedback2])
db.session.add_all([
  university1, 
  university2, 
  university3, 
  university4, 
  university5, 
  university6,
  university7
])


db.session.commit()