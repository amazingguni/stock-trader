from flask import Flask, Response
from flask_login import LoginManager
from flask_cors import CORS


from container import Container
from config import get_config_by_env
from web.admin import admin

from mongodb import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    @app.route('/')
    # pylint: disable=unused-variable
    def index():
        return Response(status=200)

    app.config.from_object(get_config_by_env())
    CORS(app)

    login_manager.init_app(app)

    container = Container()
    app.container = container
    from web.admin import views as admin_views
    views = [admin_views]
    with app.app_context():
        container.wire(modules=views)
    admin.init_app(app)
    db.init_app(app)
    return app


@login_manager.user_loader
def load_user(user_id):
    from core.user.domain.user import User
    return User.query.filter(User.id == user_id).first()
