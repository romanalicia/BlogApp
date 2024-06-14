from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Posts, User
from .import db

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@views.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/posts", methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            posts = Posts(text=text, author=current_user.id)
            db.session.add(posts)
            db.session.commit()
            flash('Post created!', category='success')
        return redirect(url_for('views.posts'))

    return render_template("posts.html", user=current_user)
