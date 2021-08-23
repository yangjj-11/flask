from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app

from flask_login import login_user, logout_user

from flaskr.models.user import User, db


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first():
            error = f'User {username} is already registered.'
        if not error:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f'Register new user {username}.')
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user, remember=True)
            current_app.logger.debug(f'Login user {username} success.')
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('blog.index')
            return redirect(next_url)
        else:
            error = 'Incorrect username or password'
            flash(error)
    return render_template('auth/login.html')


@auth.route('/logout', endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('blog.index'))