from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from flaskr.models.blog import Post, sql_db


# 有蓝图但是没有前缀/blog
blog = Blueprint('blog', __name__)


@blog.route('/', endpoint='index')
@login_required
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@blog.route('/create', methods=['GET', 'POST'], endpoint='create')
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            msg = 'Title is required.'
        if not msg:
            post = Post(title=title, body=body, author_id=current_user.id)
            sql_db.session.add(post)
            sql_db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(msg)

    return render_template('blog/create.html')


@blog.route('/<int:post_id>/update', methods=['GET', 'POST'], endpoint='update')
@login_required
def update(post_id):
    post = Post.query.get(post_id)
    if post is None:
        abort(404, f'Post id {post_id} doesn\'t exists.')
    if post.author_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        msg = None
        if not title:
            msg = 'Title is required.'
        if not msg:
            post.title = title
            post.body = body
            sql_db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(msg)

    return render_template('blog/update.html', post=post)


# delete button is a field of form, so here using post
@blog.route('/<int:post_id>/delete', methods=['POST'], endpoint='delete')
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if post is None:
        abort(404, f'Post id {post_id} doesn\'t exists.')
    if post.author_id != current_user.id:
        abort(403)
    sql_db.session.delete(post)
    sql_db.session.commit()
    return redirect(url_for('blog.index'))
