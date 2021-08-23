import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

sql_db = SQLAlchemy()
migrate = Migrate(db=sql_db)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config=None):
    app = Flask(__name__)

    config_name = config or os.environ.get('FLASK_ENV') or 'default'
    app.config.from_object(config[config_name])

    sql_db = sql_db.init_app(app)
    migrate = migrate.init_app(app)
    login_manager = login_manager.init_app(app)

    from flaskr.views import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    from flaskr.commands import init_db_command, generate_fake_data
    app.cli.add_command(init_db_command)
    app.cli.add_command(generate_fake_data)
    return app