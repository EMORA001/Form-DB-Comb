from flask import Blueprint, render_template
from flask_login import login_required, current_user
from base64 import b64encode
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('signup.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user_name=current_user.email, IMG=b64encode(current_user.imagen).decode("utf-8"))
