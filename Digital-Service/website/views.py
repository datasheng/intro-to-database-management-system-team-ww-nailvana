from flask import Blueprint, render_template, request, flash, jsonify, Flask
from flask_login import login_required, current_user
from flask_sqlalchemy  import SQLAlchemy
import sqlalchemy
from datetime import datetime, timedelta, date
import calendar
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
    type = current_user_logged_in()

    return render_template("home.html", user=current_user, type=type)


@views.route("/nailtechnicians")
def nailtechnicians():
    providers = Provider.query.filter_by(Industry="Nail Technician").all()
    return render_template("providers.html", user=current_user, providers=providers)

@views.route("/petsitters")
def petsitters():
    providers = Provider.query.filter_by(Industry="Sitter").all()
    return render_template("providers.html", user=current_user, providers=providers)

@views.route("/providers")
def providers():
    providers = Provider.query.all()
    return render_template("providers.html", user=current_user, providers=providers)


# @views.route("/provider/<int:provider_id>")
# def provider(provider_id):
#     provider = Provider.query.get_or_404(provider_id)
#     schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()
#     return render_template(
#         "provider.html", user=current_user, provider=provider, schedule=schedule
#     )


# @views.route("/provider/<int:provider_id>", methods=["POST", "GET"])
# def getappointment(provider_id):
#     provider = Provider.query.get_or_404(provider_id)
#     schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()
#     form = BookingForm()
#     args = []
#     start_time = request.form["start_time"]
#     end_time = request.form["end_time"]
#     args.append((start_time))
#     args.append((end_time))
#     args.append((provider_id))
#     results = check_provider(args)

#     if not results[0]:
#         return render_template(
#             "provider.html",
#             user=current_user,
#             provider=provider,
#             schedule=schedule,
#             status="No appointment available",
#         )
#     else:
#         return render_template(
#             "pass.html",
#             user=current_user,
#             start_time=start_time,
#             end_time=end_time,
#             results=results,
#         )

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


def get_dropdown_values(provider_id):

    schedules = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()
    myDict = {}
    for p in schedules:
    
        day = p.Day

        # Select all schedule entries that belong to a provider
        q = ProviderSchedule.query.filter_by(ProviderID=provider_id, Day = day, Availability = None).all()
    
        # build the structure (lst_c) that includes the time slots that belong to a specific date 
        lst_c = []
        if q: 
            for c in q:
                start_time = str(c.StartTime.time())[0:5]
                lst_c.append( datetime.datetime.strptime(start_time, "%H:%M").strftime("%I:%M %p") )
            myDict[day] = lst_c
        else:
            lst_c.append("No available times")
            myDict[day] = lst_c
    

    class_entry_relations = myDict
                        
    return class_entry_relations


@views.route('/_update_dropdown')
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)
    provider_id = request.args.get('provider_id', type=int)

    # get values for the second dropdown
    updated_values = get_dropdown_values(provider_id)[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)

@views.route("/provider/<int:provider_id>", methods=["POST", "GET"])
def index(provider_id):

    #initialize drop down menus

    provider = Provider.query.get_or_404(provider_id)
    schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()

    class_entry_relations = get_dropdown_values(provider_id)

    default_classes = list(class_entry_relations.keys())
    if class_entry_relations:
        default_values = class_entry_relations[default_classes[0]]
    else: 
        default_values = []

    return render_template(
        'provider.html', all_classes=default_classes, all_entries=default_values, 
        user = current_user, provider=provider, schedule=schedule, provider_id=provider_id)
                       

@views.route('/_process_data')
def process_data():
    selected_date = request.args.get('selected_class', type=str)
    selected_time = request.args.get('selected_entry', type=str)
    provider_id = request.args.get('provider_id', type=int)

    
    appointment = ProviderSchedule.query.filter_by(ProviderID=provider_id, Day = selected_date, ).first()
    appointment.Availability = 1
    db.session.commit()

    return jsonify(random_text="You selected the appointment: {} and the time: {}, appointment {}.".format(selected_date, selected_time, appointment))



