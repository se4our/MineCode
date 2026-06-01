from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

       with app.app_context():
        db.create_all()

    return app

routes.py

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='MineCode - Главная')

@main.route('/fundamentals')
def fundamentals():
    # Глубокая теория по устройству команд
    return render_template('fundamentals.html', title='Теория команд Minecraft', body_class='basic-bg')
