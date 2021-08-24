from datetime import datetime
from flaskr import sql_db
from flaskr.models.auth import User


class Post(sql_db.Model):
    __tablename__ = "posts"

    id = sql_db.Column(sql_db.Integer, primary_key=True, autoincrement=True)
    author_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey(User.id))
    created = sql_db.Column(sql_db.DateTime, nullable=False, default=datetime.utcnow)
    title = sql_db.Column(sql_db.String(64), nullable=False)
    body = sql_db.Column(sql_db.Text, nullable=False)

    def __repr__(self):
        return f"<Post ({self.id}, {self.title})>"
