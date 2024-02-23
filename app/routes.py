from app import app, db
from flask import render_template, request, redirect, url_for,flash,session
from app.models import User


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
            return redirect(url_for('dashboard'))
            
        else:
            return "Invalid username or security answer."
    return render_template('forgot_password.html')

@app.route('/dashboard/<username>', methods=['GET'])
def dashboard(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return "User not found."