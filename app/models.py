from app.database import db
from flask_login import UserMixin


# Definindo o modelo de dados
class user(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # password = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, username, password_hash):
        self.name = name
        self.email = email
        self.username = username
        self.password_hash = password_hash
        # super().__init__()

    def __repr__(self):
        return '<User %r>' % self.username

class vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    mark = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(25), nullable=False)
    type_vehicles= db.Column(db.String(30), nullable=False)
    exchange = db.Column(db.String(15), nullable=False)
    vehicle_situation = db.Column(db.String(15), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    plate = db.Column(db.String(7), nullable=False)

    def __repr__(self):
        return f'<Vehicle {self.id}>'