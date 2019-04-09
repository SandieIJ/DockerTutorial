from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from user import User
from datetime import datetime

app = Flask(__name__)
URI = 'postgresql://cs162_user:cs162_password@db/cs162'
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    value = db.Column(db.Numeric)
    now = db.Column(db.TIMESTAMP)


db.create_all()
db.session.commit()


# ------------- REGISTER -----------------------------------------------
# User Regstration
@app.route('/', methods=('GET','POST'))
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['Password']
        new_user = User.query.filter_by(email=email).first()
        error = None

        if not email:
            error = 'Email is required to register'
        elif not password:
            error = 'Password is required to register'
        elif new_user is not None:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            register_user = User(email,generate_password_hash(password))
            session.add(register_user)
            return redirect(url_for('homepage'))

    return redirect(url_for('register', error=error))

# ------------- LOGIN ----------------------------------------------
# Login
@app.route('/login', methods=('GET','POST'))

def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['Password']
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Email is not registered'
        elif not check_password_hash(user['Password'],password):
            error = 'Incorrect password, try again'
        
        if error is None:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('homepage'))
    return render_template('login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were successfully logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000)