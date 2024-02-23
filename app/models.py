from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    security_answer = db.Column(db.String(255), nullable=False)

    #def __repr__(self):
        #return '<User %r>' % self.username

    '''@classmethod
    def create_classmethod(cls,username,email,password,security_answer):
        user=User()
        user.username=username
        user.email=email
        user.password=password
        user.security_answer=security_answer
        db.session.add(user)
        db.session.commit()
        return user'''