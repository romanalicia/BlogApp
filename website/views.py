from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Notes
from .import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/notes", methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        notes = request.form.get('notes')  # Gets the post from HTML
        if len(notes) < 1:
            flash("Note is too short!", category='error')
        else:
            # providing the schema for the post
            new_note = Notes(data=notes, user_id=current_user.id)
            db.session.add(new_note)  # adding the post to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)


@views.route('/delete-notes', methods=['POST'])
def delete_notes():
    notes = json.loads(request.data)
    notesId = notes['notesId']
    notes = Notes.query.get(notesId)
    if notes:
        if notes.user_id == current_user.id:
            db.session.delete(notes)
            db.session.commit()
    return jsonify({})
