from app import app, db
from flask import render_template, request, redirect, url_for,flash,session,jsonify
from app.models import User, Movie_Data, Wishlist, UserPreferences
from sqlalchemy.sql import text,or_,func
from math import ceil 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        security_answer=request.form['security_answer']
        # Create a new user object and add it to the database
        new_user = User(username=username, email=email, password=password,security_answer=security_answer)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('preferences'))
    return render_template('signup.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    username = session.get('username')
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first() # Assuming you're using Flask-Login for user authentication
        genre = request.form.getlist('genres')  # Assuming multiple genres can be selected
        director = request.form.getlist('directors')  # Assuming multiple directors can be selected
        actor = request.form.getlist('actors')  # Assuming multiple actors can be selected
        year = request.form.getlist('years')  # Assuming multiple years can be selected
        # Create a new UserPreferences object and add it to the database for each preference selected
        for g in genre:
            for d in director:
                for a in actor:
                    for y in year:
                        preferences = UserPreferences(user_id=user.id, genre=g, director=d, actor=a, year=y)
                        db.session.add(preferences)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('preferences.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Authentication successful, store user id in session
            session['username'] = user.username
            return redirect(url_for('dashboard', username=user.username))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        security_answer = request.form['security_answer']
        user = User.query.filter_by(username=username, security_answer=security_answer).first()
        if user:
            # Implement password reset logic
            return redirect(url_for('dashboard', username=user.username))  # Pass the username to the dashboard route
            
        else:
            return "Invalid username or security answer."
    return render_template('forgot_password.html')

'''@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_info = {'username': user.username, 'email': user.email}
        query = text("SELECT Title, Description FROM Movie_Data WHERE Year = 2024 LIMIT 5")
        result = db.session.execute(query)
        upcoming_movies = result.fetchall()
        upcoming_movies_list = upcoming_movies

        return render_template('dashboard.html', user=user_info, upcoming_movies=upcoming_movies_list)
    else:
        return "User not found."'''

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_info = {'username': user.username, 'email': user.email}
        # Fetch upcoming movies
        query = text("SELECT Title, Description FROM Movie_Data WHERE Year = 2024 LIMIT 5")
        result = db.session.execute(query)
        upcoming_movies = result.fetchall()
        # Fetch user preferences
        user_preferences = UserPreferences.query.filter_by(user_id=user.id).first()
        # Filter movies based on user preferences
        if user_preferences:
            preferred_genre = user_preferences.genre
            preferred_director = user_preferences.director
            preferred_actor = user_preferences.actor
            # Query movies with highest ratings (over 7.5) matching user preferences
            recommended_movies = Movie_Data.query.filter(
                (Movie_Data.Genre == preferred_genre) |
                (Movie_Data.Director == preferred_director) |
                (Movie_Data.Actors.like(f"%{preferred_actor}%"))
            ).filter(Movie_Data.Rating > 7.5).order_by(Movie_Data.Rating.desc()).limit(10).all()
            
            query_trending_movies = text("SELECT * FROM Movie_Data WHERE Metascore >= 75 AND Rating > 7 ORDER BY Metascore DESC, Rating DESC LIMIT 10")
            result_trending_movies = db.session.execute(query_trending_movies)
            trending_movies = result_trending_movies.fetchall()

            print("Trending movies:", trending_movies)  # Debugging statement
            
        else:
            # If no user preferences found, recommend top-rated movies
            recommended_movies = Movie_Data.query.filter(Movie_Data.Rating > 7.5).order_by(
                Movie_Data.Rating.desc()).limit(10).all()
            query_trending_movies = text("SELECT * FROM Movie_Data WHERE Metascore >= 75 AND Rating > 7 ORDER BY Metascore DESC, Rating DESC LIMIT 10")
            result_trending_movies = db.session.execute(query_trending_movies)
            trending_movies = result_trending_movies.fetchall()

            print("Trending movies:", trending_movies)  # Debugging statement
            
        return render_template('dashboard.html', user=user_info, upcoming_movies=upcoming_movies, recommended_movies=recommended_movies,trending_movies=trending_movies)
    else:
        return "User not found."

    

'''@app.route('/search_movies/<username>', methods=['GET', 'POST'])
def search_movies(username):
    if request.method == 'GET':
        query = request.args.get('query')
        if query:
            # Perform the search query
            search_results = Movie_Data.query.filter(Movie_Data.Title.ilike(f'%{query}%')).all()
            return render_template('search_results.html', user=username, search_results=search_results)
        else:
            # If no query is provided, return an empty list
            return render_template('search_results.html', user=username, search_results=[])
    else:
        return "Invalid request method."'''

@app.route('/search_movies/<username>', methods=['GET', 'POST'])
def search_movies(username):
    #user = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        query = request.args.get('query')
        if query:
            # Perform the search query
            search_results = Movie_Data.query.filter(Movie_Data.Title.ilike(f'%{query}%')).all()
            return render_template('search_results.html', user=username, search_results=search_results)
        else:
            # If no query is provided, return an empty list
            return render_template('search_results.html', user=username, search_results=[])
    elif request.method == 'POST':
        # Get the movie rank from the form data
        movie_rank = request.form.get('movie_rank')
        if movie_rank:
            # Find the movie in the database
            movie = Movie_Data.query.filter_by(Rank=movie_rank).first()
            if movie:
                # Add the movie to the user's wishlist
                user = User.query.filter_by(username=username).first()
                if user:
                    wishlist_entry = Wishlist(user_id=user.id, movie_rank=movie.Rank)
                    db.session.add(wishlist_entry)
                    db.session.commit()
                    #return jsonify({'message': 'Movie added to wishlist successfully'})
                    return redirect(url_for('search_movies', username=user.username)) 
                else:
                    return jsonify({'error': 'User not found'}), 404
            else:
                return jsonify({'error': 'Movie not found'}), 404
        else:
            return jsonify({'error': 'Invalid request'}), 400
    else:
        return jsonify({'error': 'Invalid request method'}), 405


def get_wishlist_data(username):
    # Query the database to fetch wishlist data for the user with the given username
    user = User.query.filter_by(username=username).first()
    if user:
        wishlist_data = Wishlist.query.filter_by(user_id=user.id).all()
        return wishlist_data
    else:
        return []  

@app.route('/wishlist_page/<username>', methods=['GET', 'POST'])
def wishlist_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        wishlist_data = get_wishlist_data(username)
        # Fetch movie details for each wishlist entry
        for entry in wishlist_data:
            entry.movie = Movie_Data.query.filter_by(Rank=entry.movie_rank).first()
        return render_template('wishlist.html', user=user, wishlist_data=wishlist_data)
    else:
        return "User not found."

'''@app.route('/show_movies', methods=['GET'])
def show_movies():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Query database to get movies for the current page
    movies = Movie_Data.query.paginate(page=page, per_page=per_page)

    # Calculate total number of pages
    total_pages = ceil(movies.total / per_page)

    return render_template('show_movies.html', movies=movies, page=page, total_pages=total_pages)'''

@app.route('/movie/<string:Rank>')
def movie_page(Rank):
    # Retrieve the movie details from the database based on the product ID
    movie = Movie_Data.query.filter_by(Rank=Rank).first()
    if movie is None:
        abort(404)
    return render_template('movie.html', movie=movie)

@app.route('/movie/<string:Rank>/rate_review', methods=['GET', 'POST'])
def movie_rating_review(Rank):
    if request.method == 'POST':
        rating = request.form.get('rating')
        review = request.form.get('review')
        # Process rating and review data, e.g., save to database
        return 'Rating: {}, Review: {}'.format(rating, review)
    return render_template('rate_review.html', Rank=Rank)


@app.route('/search', methods=['GET'])
def search():
    #user = User.query.filter_by(username=username).first()
    # Get the search query from the request
    query = request.args.get('query', '')

    # Get filter options from the request
    Genre = request.args.get('Genre')
    Actor = request.args.get('Actor')
    Rating = request.args.get('Rating')

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query for products
    query_base = Movie_Data.query

    # Apply filters if provided
    if Actor:
        # Split the actor string and filter by each individual actor
        actors = Actor.split(", ")
        actor_filters = [Movie_Data.Actors.ilike(f'%{actor}%') for actor in actors]
        query_base = query_base.filter(or_(*actor_filters))

    if Genre:
        # Split the genre string and filter by each individual genre
        genres = Genre.split(",")
        genre_filters = [Movie_Data.Genre.ilike(f'%{genre}%') for genre in genres]
        query_base = query_base.filter(or_(*genre_filters))

    if Rating:
        query_base = query_base.filter(Movie_Data.Rating >= int(Rating))

    # Filter products based on search query
    if query:
        # If both query and filters are provided, filter by both
        query_results = query_base.filter(or_(Movie_Data.Title.ilike(f'%{query}%'), Movie_Data.Description.ilike(f'%{query}%')))
    else:
        # If only filters are provided, use filtered query
        query_results = query_base

    # Paginate the results
    movies = query_results.paginate(page=page, per_page=per_page)

    # Calculate total number of pages
    total_pages = movies.total // per_page + (movies.total % per_page > 0)

    # Fetch unique genres and actors from the database
    genres = set()
    actors = set()
    for movie in movies.items:
        genres.update(movie.Genre.split(","))
        actors.update(movie.Actors.split(", "))
        actors.update(movie.Actors.split(","))

    return render_template('show_movies.html',movies=movies, page=page, total_pages=total_pages, genres=genres, actors=actors)



@app.route('/movies_genre')
def movies_genre():
    # Query movies grouped by genre
    movies_by_genre = {}
    movies = Movie_Data.query.all()
    
    for movie in movies:
        genres = movie.Genre.split(',')  # Split the genres into a list
        for genre in genres:
            genre_movies = movies_by_genre.get(genre, [])  # Get movies list for the current genre
            if len(genre_movies) < 7:
                genre_movies.append(movie)  # Append the current movie to the genre's movies list
                movies_by_genre[genre] = genre_movies  # Update the movies by genre dictionary
    
    return render_template('movies_by_genre.html', movies_by_genre=movies_by_genre)