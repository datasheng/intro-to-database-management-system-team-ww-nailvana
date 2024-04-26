from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from .auth import *
from . import db
import json

# standard routes for users
# Blueprint: many routes defined within
views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user=current_user)

# @views.route("/providers")
# def providers():
#     return render_template("providers.html", user=current_user)

@views.route("/providers")
def providers():
    providers = Provider.query.all()  
    return render_template("providers.html", user=current_user, providers=providers)

@views.route("/provider/<int:provider_id>", methods=['POST', 'GET'])
def provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    return render_template("provider.html", user=current_user, provider=provider)

@views.route("/appointmentbooked", methods=['POST', 'GET'])
def appointmentbooked():
    return render_template("appointmentbooked.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
