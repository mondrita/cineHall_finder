from app import db
class Movie_Data(db.Model):
    __tablename__ = 'Movie_Data'
    Rank = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Text)
    Genre = db.Column(db.Text)
    Description = db.Column(db.Text)
    Director = db.Column(db.Text)
    Actors = db.Column(db.Text)
    Year = db.Column(db.Integer)
    Runtime = db.Column(db.Integer)
    Rating = db.Column(db.Numeric)
    Votes = db.Column(db.Integer)
    Revenue = db.Column(db.Text)
    Metascore = db.Column(db.Integer)

    def __repr__(self):
        return f"<MovieData(title='{self.Title}', year='{self.Year}')>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    security_answer = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_rank = db.Column(db.Integer, db.ForeignKey('Movie_Data.Rank'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Corrected reference to 'user' table
    # Define the relationship with User
    user = db.relationship('User', backref=db.backref('wishlist', lazy=True))

    def __repr__(self):
        return f"<WishlistEntry(movie_rank={self.movie_rank}, user_id={self.user_id})>"
