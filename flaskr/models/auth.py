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


# 提供一个 user_loader 回调，此回调用于从会话中存储的用户 ID 重新加载用户对象。它应该采用用户的 unicode ID，并返回相应的用户对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
