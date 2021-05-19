from flask import Flask, Response
from flask_login import LoginManager
from flask_cors import CORS


from config import get_config_by_env
from web.admin import admin

from mongodb import db
from container import container

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='./web/templates')

    @app.route('/')
    # pylint: disable=unused-variable
    def index():
        return Response(status=200)

    app.config.from_object(get_config_by_env())
    CORS(app)

    login_manager.init_app(app)

    app.container = container

    from web.stock import views as stock_views
    views = [stock_views]
    register_blueprints(app, views)

    from web.admin.views import crawl as admin_crawl_views
    from web.admin.views import portfolio as admin_portfolio_views

    admin_views = [admin_crawl_views, admin_portfolio_views, ]

    with app.app_context():
        container.wire(modules=views)
        container.wire(modules=admin_views)
    admin.init_app(app)
    db.init_app(app)
    return app


def register_blueprints(app, views):
    for view in views:
        app.register_blueprint(view.bp)


@login_manager.user_loader
def load_user(user_id):
    from core.user.domain.user import User
    return User.query.filter(User.id == user_id).first()


app = create_app()
