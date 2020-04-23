import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost_proyecto.sqlite"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    # birthdate = db.Column(db.String)
    birthdate = db.Column(db.DateTime)
    password = db.Column(db.String)
    photo = db.Column(db.String)


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    titulo = db.Column(db.String)
    notas = db.Column(db.String)
    user_id = db.Column(db.Integer)



def comprueba_usuario(db, username, password):
    user = db.query(User).filter_by(user_name=username, password=password).first()