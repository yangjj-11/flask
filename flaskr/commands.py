import click
from flask.cli import with_appcontext

from flaskr.models.auth import User, sql_db
from flaskr.models.blog import Post
from random import randrange
from faker import Faker

# from sqlalchemy.exc import IntegrityError


# 使用flask默认的app.cli.command()装饰器添加的命令z执行时自动推入应用上下文
# 使用click的command不会，要想达到相同的效果使用with_appcontext,否则不注册到app上会报错
@click.command("init-db")
@with_appcontext
def init_db_command():
    sql_db.drop_all()
    sql_db.create_all()
    click.echo("Initialized the database.")


@click.command("fake")
@with_appcontext
def generate_fake_data():
    # fake = Faker("zh_CN")伪造中文，默认en_US
    fake = Faker()
    i = 0
    while i < 5:
        u = User(username=fake.user_name(), password="cat")
        sql_db.session.add(u)
        try:
            sql_db.session.commit()
            i += 1
        except Exception as e:
            print(e)
            sql_db.session.rollback()

    user_count = User.query.count()
    i = 0
    while i < 20:
        p = Post(
            title=fake.sentence(nb_words=randrange(1, 5)),
            body=fake.text(),
            created=fake.past_date(),
            author=User.query.offset(randrange(0, user_count)).first(),
        )
        sql_db.session.add(p)
        try:
            sql_db.session.commit()
            i += 1
        except Exception as e:
            print(e)
            sql_db.session.rollback()
    click.echo("Generated 5 fake users and 20 posts.")
