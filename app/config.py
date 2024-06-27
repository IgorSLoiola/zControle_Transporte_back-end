import os

class Config:
    conexao = 'sqlite:///db.sqlite3'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = conexao
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # App.config['SQLALCHEMY_DATABASE_URI'] = conexao
    # App.config['SECRET_KEY'] = 'minha-chave'
    # App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
