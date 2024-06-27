from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from app.routes import approutes
from app.database import db
from app.config import Config

def create_app(config_class=Config):
    App = Flask(__name__)
    #config
    App.config.from_object(config_class)
    #database
    db.init_app(App)
    migrate = Migrate(App, db)
    #ajuda a encontra os dados do react
    cors = CORS(App, resources={r"/*": {"origins": "http://localhost:3000"}})
    # rotas
    App.register_blueprint(approutes, url_prefix='/')

    # Criação do objeto LoginManager
    login_manager = LoginManager()

    # Inicialização do LoginManager
    login_manager.init_app(App)

    return App
