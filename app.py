from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

from .container import Container

db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()


def create_app(config_name='config.development.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_name)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    container = Container(session=db.session)
    app.container = container

    # with app.app_context():
    #     container.wire(modules=views)
    return app


@login_manager.user_loader
def load_user(user_id):
    from core.user.domain.user import User
    return User.query.filter(User.id == user_id).first()
