from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')



    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "Silahkan login terlebih dahulu."
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)


    #sementara :P
    @app.route('/')
    def joss_pokoke():
        return 'Josss, Its Work jarx...'

    return app