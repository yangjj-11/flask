from flaskr.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

sql_db = SQLAlchemy()
migrate = Migrate(db=sql_db)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app(conf=None):
    global sql_db, migrate, login_manager
    app = Flask(__name__)

    app.config.from_object(config[conf])

    sql_db = sql_db.init_app(app)
    migrate = migrate.init_app(app)
    login_manager = login_manager.init_app(app)

    from flaskr.api.auth import auth
    from flaskr.api.blog import blog

    app.register_blueprint(auth)
    app.register_blueprint(blog)

    from flaskr.commands import init_db_command, generate_fake_data

    app.cli.add_command(init_db_command)
    app.cli.add_command(generate_fake_data)
    return app
