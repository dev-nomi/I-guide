from app import db, User, Feedback

db.drop_all()
db.create_all()

user1 = User(name="noman", email="noman@gmail.com", password="123456")
user2 = User(name="noman khalid", email="noman@khalid.com", password="123456")

feedback1 = Feedback(content='First feedback', rating=3, user=user1)
feedback2 = Feedback(content='Second feedback', rating=1, user=user1)


db.session.add_all([user1,user2])
db.session.add_all([feedback1, feedback2])

db.session.commit()