from flask import Blueprint, render_template, request, flash, jsonify, Flask
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
    # if request.method == "POST":
    #     note = request.form.get("note")

    #     if len(note) < 1:
    #         flash("Note is too short!", category="error")
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash("Note added!", category="success")

    return render_template("home.html", user=current_user)


@views.route("/providers")
def providers():
    providers = Provider.query.all()
    return render_template("providers.html", user=current_user, providers=providers)


@views.route("/provider/<int:provider_id>")
def provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()
    return render_template(
        "provider.html", user=current_user, provider=provider, schedule=schedule
    )


@views.route("/provider/<int:provider_id>", methods=["POST", "GET"])
def getappointment(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()
    form = BookingForm()
    args = []
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    args.append((start_time))
    args.append((end_time))
    args.append((provider_id))
    results = check_provider(args)

    if not results[0]:
        return render_template(
            "provider.html",
            user=current_user,
            provider=provider,
            schedule=schedule,
            status="No appointment available",
        )
    else:
        return render_template(
            "pass.html",
            user=current_user,
            start_time=start_time,
            end_time=end_time,
            results=results,
        )

    # if

    # add check; only customers should make appointments, only providers edit the schedule
    # if form.validate_on_submit():
    #     date = datetime.now(datetime.UTC).date()  # current date
    #     appointment_date = form.get_datetime(date)  # TODO: check if this is redundant

    #     appointment = NailAppointment(
    #         CustomerID=current_user.CustomerID,
    #         ProviderID=provider_id,
    #         Status="Scheduled",  # possible status codes: scheduled, fulfilled, cancelled(?)
    #         StartTime=appointment_date,
    #         EndTime=appointment_date + timedelta(hours=2),  # each appmt is 2 hours long
    #     )
    #     db.session.add(appointment)
    #     db.session.commit()

    #     flash("Appointment booked!", "success")
    # return render_template(
    #     "pass.html", user=current_user, start_time=start_time, end_time=end_time, results = results
    # )


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
    # return customerNames
    return render_template(
        "sql-customer-data.html", user=current_user, customerNames=customerNames
    )


# @views.route('/test')
# def test():
#      return render_template("test.html", user=current_user)

# @views.route('/test', methods = ["POST"])
# def getvalue():
#     start_time = request.form['start_time']
#     end_time = request.form['end_time']
#     args = []
#     args.append((start_time))
#     args.append((end_time))
#     results = check_availability(args)
#     return render_template("pass.html", user=current_user, start_time=start_time, end_time=end_time, results = results)
