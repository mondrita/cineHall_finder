from app import app,db
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
    pic = db.Column(db.Text)

    def __repr__(self):
        return f"<hall(Movie_Title='{self.Movie_Title}', Location='{self.Location}', Start_Date='{self.Start_Date}')>"
    

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.Integer, db.ForeignKey('hall.Movie_Title'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='available')  # 'available' or 'taken'

    def __repr__(self):
        return f"<Seat(movie_id={self.movie_id}, seat_number='{self.seat_number}', status='{self.status}')>"



def populate_seats(movie_title, total_seats):
    # Retrieve the movie from the database
    movie = hall.query.filter_by(Movie_Title=movie_title).first()

    # Check if the movie exists
    if movie:
        # Check if seats already exist for the movie
        existing_seats = Seat.query.filter_by(movie_title=movie_title).count()
        if existing_seats == 0:
            # Generate and add seats for the movie
            for seat_number in range(1, total_seats + 1):
                seat = Seat(movie_title=movie_title, seat_number=str(seat_number))
                db.session.add(seat)
            
            # Commit the changes to the database
            db.session.commit()
            print(f"Seats added for movie: '{movie_title}'")
        else:
            print(f"Seats already exist for movie: '{movie_title}'")
    else:
        print(f"Movie '{movie_title}' not found in the database.")

movies = {
    "Avengers: Endgame": 20,
    "Spider-Man: Far From Home": 20,
    "The Lion King": 20,
    "Joker": 20,
    "Frozen II": 20,
    "Fast & Furious 9": 20,
    "The Matrix Resurrections": 20,
    "Black Widow": 20,
    "Wonder Woman 1984": 20,
    "No Time to Die": 20,
    "Tenet": 20,
    "The Suicide Squad": 20,
    "Godzilla vs. Kong": 20,
    "Dune": 20,
    "Shang-Chi and the Legend of the Ten Rings": 20,
    "Black Panther": 20,
    "The Dark Knight": 20,
    "Inception": 20,
    "Interstellar": 20,
    "Titanic": 20
}



with app.app_context():
    for movie_title, total_seats in movies.items():
        populate_seats(movie_title, total_seats)


class Hall_Details(db.Model):
    __tablename__ = 'hall_details'
    hall_id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    direction = db.Column(db.Text, nullable=False)
    parking_lot_capacity = db.Column(db.Integer)
    food_court_items = db.Column(db.Text)

    def __repr__(self):
        return f"<hall_details(Hall_Name='{self.hall_name}', Location='{self.location}', Direction='{self.direction}', Parking_Lot_Capacity='{self.parking_lot_capacity}', Food_Court_Items='{self.food_court_items}')>"
