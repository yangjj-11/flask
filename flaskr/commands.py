import click
from flask.cli import with_appcontext

from flaskr.models.auth import User, sql_db
from flaskr.models.blog import Post


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Initialize database. """
    sql_db.drop_all()
    sql_db.create_all()
    click.echo('Initialized the database.')


@click.command('fake')
@with_appcontext
def generate_fake_data():
    """ Generate fake data. """
    from random import randrange
    from faker import Faker
    from sqlalchemy.exc import IntegrityError
    fake = Faker()

    i = 0
    while i < 5:
        u = User(username=fake.user_name(), password='cat')
        sql_db.session.add(u)
        try:
            sql_db.session.commit()
            i += 1
        except IntegrityError:
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
        except IntegrityError:
            sql_db.session.rollback()

    click.echo('Generated 5 fake users and 20 posts.')