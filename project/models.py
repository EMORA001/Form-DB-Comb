from flask_login import UserMixin
from datetime import datetime
from . import db
import pytz

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(30))
    name = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    edad = db.Column(db.String(3))
    tipo = db.Column(db.String(15))
    user_agent = db.Column(db.String(50))
    client_ip = db.Column(db.String(25))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Guayaquil')))
    imagen = db.Column(db.LargeBinary)
