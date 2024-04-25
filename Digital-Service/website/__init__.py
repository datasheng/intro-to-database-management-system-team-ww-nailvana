from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_login import current_user

db = SQLAlchemy()
DB_NAME = "catcare"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "adjalksdjsa ldksjadklsajd"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql://root:databases336@localhost/{DB_NAME}"
    )

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Provider, Customer, User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = Provider.query.get(int(id))
        if user is None:
            user = Customer.query.get(int(id))
        return user

    return app
