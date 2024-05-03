from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from .models import *
from .auth import *
from .forms import BookingForm
from . import db
import json
from .createDB import *

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


@views.route("/providers")
def providers():
    providers = Provider.query.all()
    return render_template("providers.html", user=current_user, providers=providers)


@views.route("/provider/<int:provider_id>", methods=["POST", "GET"])
def provider(provider_id):
    form = BookingForm()
    provider = Provider.query.get_or_404(provider_id)
    schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()

    # add check; only customers should make appointments, only providers edit the schedule
    if form.validate_on_submit():
        date = datetime.now(datetime.UTC).date()  # current date
        appointment_date = form.get_datetime(date)  # TODO: check if this is redundant

        appointment = NailAppointment(
            CustomerID=current_user.CustomerID,
            ProviderID=provider_id,
            Status="Scheduled",  # possible status codes: scheduled, fulfilled, cancelled(?)
            StartTime=appointment_date,
            EndTime=appointment_date + timedelta(hours=2),  # each appmt is 2 hours long
        )
        db.session.add(appointment)
        db.session.commit()

        flash("Appointment booked!", "success")
    return render_template(
        "provider.html", user=current_user, provider=provider, schedule=schedule
    )


@views.route("/appointmentbooked", methods=["POST", "GET"])
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


@views.route("/provider-data")
def providerdata():
    sql_provider()
    return render_template("sql-provider-data.html", user=current_user)


@views.route("/customer-data")
def customerdata():
    customerNames = sql_customer()
    sql_stored_procedure()
    # return customerNames
    return render_template(
        "sql-customer-data.html", user=current_user, customerNames=customerNames
    )
