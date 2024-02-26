from app import app, db
from flask import render_template, request, redirect, url_for,flash,session,jsonify
from app.models import User, Movie_Data, Wishlist
from sqlalchemy.sql import text,or_


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
        return redirect(url_for('preferences'))
    return render_template('signup.html')
@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
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

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
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
