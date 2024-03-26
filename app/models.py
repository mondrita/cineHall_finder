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
    username = db.Column(db.String(80), unique=True, nullable=False)
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
class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    genre = db.Column(db.String(50))  # Assuming maximum genre length is 50 characters
    director = db.Column(db.String(100))  # Assuming maximum director name length is 100 characters
    actor = db.Column(db.String(100))  # Assuming maximum actor name length is 100 characters
    year = db.Column(db.Integer)  # Year preference
    def __repr__(self):
        return f"<UserPreferences(user_name={self.user_name}, genre='{self.genre}', director='{self.director}', actor='{self.actor}', year={self.year})>"

class RatingReview(db.Model):
    __tablename__ = 'rating_review'
    id = db.Column(db.Integer, primary_key=True)
    movie_rank = db.Column(db.Integer, db.ForeignKey('Movie_Data.Rank'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)

    #def __repr__(self):
       # return f"<RatingReview(id='{self.id}', item_id='{self.item_id}', rating='{self.rating}', review='{self.review}')>"
    

class hall(db.Model):
    __tablename__ = 'hall'
    Movie_Title = db.Column(db.Text, primary_key=True)
    Theater = db.Column(db.Text)
    Location = db.Column(db.Text)
    Movie_time = db.Column(db.Text)
    Total_Seats = db.Column(db.Integer)
    Seats_Available = db.Column(db.Integer)
    Ticket_Price = db.Column(db.Integer)
    three_D = db.Column(db.Text)
    duration = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __repr__(self):
        return f"<hall(Movie_Title='{self.Movie_Title}', Location='{self.Location}', Start_Date='{self.Start_Date}')>"