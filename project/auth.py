from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email    = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email    = request.form.get('email')
    name     = request.form.get('name')
    apellido     = request.form.get('apellido')
    edad     = request.form.get('edad')
    password = request.form.get('password')
    tipo = request.form.get('tipo')
    
    user_agent = request.headers.get('User-Agent')

    img = request.files['file'].read()

    if request.headers.get('X-Forwarded-For'): 
        client_ip = request.headers.get('X-Forwarded-For')
    else: 
        client_ip = request.remote_addr # For local development


    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, 
                    name=name, 
                    apellido=apellido,
                    tipo = tipo,
                    edad=edad,
                    password=generate_password_hash(password, method='sha256'),
                    user_agent=user_agent,
                    client_ip=client_ip,
                    imagen=img
                    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Datos Registrados con exito.')
    return redirect(url_for('auth.signup'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))