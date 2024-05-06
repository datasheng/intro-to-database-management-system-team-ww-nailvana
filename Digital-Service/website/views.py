from flask import Blueprint, render_template, request, flash, jsonify, Flask
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
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


@views.route("/nailvana")
def nailtechnicians():
    providers = Provider.query.filter_by(Industry="Nail Technician").all()
    return render_template("nailvanaPages/nailvana.html", user=current_user, providers=providers)

@views.route("/manicure")
def manicure():
    providers = Provider.query.filter_by(Specialization="Manicure").all()
    return render_template("nailvanaPages/manicure.html", user=current_user, providers=providers)

@views.route("/pedicure-and-spa")
def pedicure():
    providers = Provider.query.filter_by(Specialization="Pedicure & Spa").all()
    return render_template("nailvanaPages/pediAndSpa.html", user=current_user, providers=providers)

@views.route("/waxing")
def waxing():
    providers = Provider.query.filter_by(Specialization="Waxing").all()
    return render_template("nailvanaPages/waxing.html", user=current_user, providers=providers)


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


@views.route("/appointmentbooked", methods=["POST", "GET"])
def appointmentbooked():
    return render_template("appointmentbooked.html", user=current_user)


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

    if schedules: 
        for p in schedules:
        
            date = p.AppointmentDate
            # Select all schedule entries that belong to a provider
            q = ProviderSchedule.query.filter_by(ProviderID=provider_id, Availability = None, AppointmentDate = date).all()
            # build the structure (lst_c) that includes the time slots that belong to a specific date 
            lst_c = []
            if q: 
                for c in q:
                    start_time = str(c.StartTime)
                    # lst_c.append( datetime.datetime.strptime(start_time, "%H:%M").strftime("%I:%M %p") )
                    lst_c.append( datetime.datetime.strptime(start_time, "%H:%M:%S").strftime("%I:%M %p") )
                    #lst_c.append( start_time )
                # myDict[str(date)] = lst_c
                myDict[str(datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%A, %B %d"))] = lst_c
            else:
                lst_c.append("No available times")
                myDict[str(date)] = lst_c

    else: 
        lst_c = []
        lst_c.append("No available times")
        myDict["No available days"] = lst_c
    

    class_entry_relations = myDict

    return class_entry_relations


@views.route("/_update_dropdown")
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get("selected_class", type=str)
    provider_id = request.args.get("provider_id", type=int)

    # get values for the second dropdown
    updated_values = get_dropdown_values(provider_id)[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ""
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@views.route("/provider/<int:provider_id>", methods=["POST", "GET"])
def index(provider_id):

    # initialize drop down menus

    provider = Provider.query.get_or_404(provider_id)
    schedule = ProviderSchedule.query.filter_by(ProviderID=provider_id).all()
    type = current_user_logged_in()

    class_entry_relations = get_dropdown_values(provider_id)

    default_classes = list(class_entry_relations.keys())
    if class_entry_relations:
        default_values = class_entry_relations[default_classes[0]]
    else:
        default_values = []

    return render_template(
        "provider.html",
        all_classes=default_classes,
        all_entries=default_values,
        user=current_user,
        provider=provider,
        schedule=schedule,
        provider_id=provider_id,
        type=type,
    )


@views.route("/_process_data")
def process_data():
    selected_date = request.args.get("selected_class", type=str)
    selected_time = request.args.get("selected_entry", type=str)
    provider_id = request.args.get("provider_id", type=int)

    


    appointment = ProviderSchedule.query.filter_by(ProviderID=provider_id, AppointmentDate = selected_date, StartTime = selected_time).first()
    appointment.Availability = 1
    db.session.commit()

    return jsonify(
        random_text="You selected the appointment: {} and the time: {}, appointment {}.".format(
            selected_date, selected_time, appointment
        )
    )
