from flaskr import create_app
from flaskr import sql_db
from flaskr.models.auth import User
from flaskr.models.blog import Post

app = create_app("development")


@app.shell_context_processor
def add_shell_context():
    return dict(db=sql_db, Post=Post, User=User)


@app.route("/test", methods=["GET"])
def test():
    return {"msg": "ok"}
