from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Posts
from .import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/posts", methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        posts = request.form.get('posts')  # Gets the post from HTML
        if len(posts) < 1:
            flash("Posts is too short!", category='error')
        else:
            # providing the schema for the post
            new_post = Posts(data=posts, user_id=current_user.id)
            db.session.add(new_post)  # adding the posts to the database
            db.session.commit()
            flash('Post posted!', category='success')

    return render_template("posts.html", user=current_user)


@views.route("/posts", methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        posts = request.form.get('posts')  # Gets the post from HTML
        if len(posts) < 1:
            flash("Post is too short!", category='error')
        else:
            # providing the schema for the post
            new_post = Posts(data=posts, user_id=current_user.id)
            db.session.add(new_post)  # adding the post to the database
            db.session.commit()
            flash('Post added!', category='success')

    return render_template("posts.html", user=current_user)


@views.route('/delete-posts', methods=['POST'])
def delete_posts():
    posts = json.loads(request.data)
    postsId = posts['postsId']
    posts = Posts.query.get(postsId)
    if posts:
        if posts.user_id == current_user.id:
            db.session.delete(posts)
            db.session.commit()
    return jsonify({})
