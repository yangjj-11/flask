from flaskr import create_app
from flaskr.models.user import sql_db, Post, User


app = create_app('development')


@app.shell_context_processor
def add_shell_context():
    return dict(db=sql_db, Post=Post, User=User)