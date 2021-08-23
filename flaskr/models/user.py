from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flaskr import sql_db, login_manager


# 使用flask_login进行用户的登录和登出管理，需要将我们的User模型继承flask_login的UserMixin基类
class User(UserMixin, sql_db.Model):
    __tablename__ = 'users'

    id = sql_db.Column(sql_db.Integer, primary_key=True, autoincrement=True)
    username = sql_db.Column(sql_db.String(32), unique=True, nullable=False)
    password_hash = sql_db.Column(sql_db.String(128))
    posts = sql_db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User ({self.id}, {self.username})>'


class Post(sql_db.Model):
    __tablename__ = 'posts'

    id = sql_db.Column(sql_db.Integer, primary_key=True, autoincrement=True)
    author_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey(User.id))
    created = sql_db.Column(sql_db.DateTime, nullable=False, default=datetime.utcnow)
    title = sql_db.Column(sql_db.String(64), nullable=False)
    body = sql_db.Column(sql_db.Text, nullable=False)

    def __repr__(self):
        return f'<Post ({self.id}, {self.title})>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_db():
    sql_db.drop_all()
    sql_db.create_all()
