import os
import pathlib
import tempfile

# Python 3.4之前和路径相关操作函数都放在os模块里面，之后添加了新模块
# 绝对地址
# os.path.dirname()去掉文件名，返回目录
abs_basedir = os.path.abspath(os.path.dirname(__file__))
tempdir = tempfile.gettempdir()

# 相对地址
# 或 from pathlib import Path
# parents[0] == parent/parents[1] == parent.parent
# rel_basedir = pathlib.Path(__file__).parents[0]


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "it is a secret"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flaskr_dev"


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SERVER_NAME = "test.flaskr"
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flaskr_test"


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flaskr_prod"


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": DevConfig,
}
