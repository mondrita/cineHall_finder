from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')

'''@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            security_answer = request.form.get('security_answer')
            new_user = User(username=username, email=email, password=password, security_answer=security_answer)
            User.create_classmethod(username,email,password,security_answer)
            return redirect(url_for('preferences'))
        return render_template('signup.html')

    except Exception as e:
        return {'message':'error'}'''

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
        # Code for handling preferences form submission and updating database omitted for brevity
        # Redirect to dashboard after submitting preferences
        return redirect(url_for('index'))

    return render_template('preferences.html')