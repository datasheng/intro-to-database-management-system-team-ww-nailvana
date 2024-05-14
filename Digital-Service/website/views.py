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
    type = current_user_logged_in()
    return render_template(
        "nailvanaPages/nailvana.html", user=current_user, providers=providers, type=type
    )


@views.route("/manicure")
def manicure():
    providers = Provider.query.filter_by(Specialization="Manicure").all()
    type = current_user_logged_in()
    return render_template(
        "nailvanaPages/manicure.html", user=current_user, providers=providers, type=type
    )


@views.route("/pedicure-and-spa")
def pedicure():
    providers = Provider.query.filter_by(Specialization="Pedicure & Spa").all()
    type = current_user_logged_in()
    return render_template(
        "nailvanaPages/pediAndSpa.html",
        user=current_user,
        providers=providers,
        type=type,
    )


@views.route("/waxing")
def waxing():
    providers = Provider.query.filter_by(Specialization="Waxing").all()
    type = current_user_logged_in()
    return render_template(
        "nailvanaPages/waxing.html", user=current_user, providers=providers, type=type
    )


@views.route("/petsitters")
def petsitters():
    providers = Provider.query.filter_by(Industry="Sitter").all()
    type = current_user_logged_in()
    return render_template(
        "providers.html", user=current_user, providers=providers, type=type
    )


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

    schedules = (
        ProviderSchedule.query.filter_by(ProviderID=provider_id)
        .order_by(ProviderSchedule.AppointmentDate)
        .all()
    )
    myDict = {}

    if schedules:
        for p in schedules:

            date = p.AppointmentDate
            # Select all schedule entries that belong to a provider
            q = (
                ProviderSchedule.query.filter_by(
                    ProviderID=provider_id, Availability=None, AppointmentDate=date
                )
                .order_by(ProviderSchedule.AppointmentDate)
                .all()
            )
            # build the structure (lst_c) that includes the time slots that belong to a specific date
            lst_c = []
            if q:
                for c in q:
                    start_time = str(c.StartTime)
                    # lst_c.append( datetime.datetime.strptime(start_time, "%H:%M").strftime("%I:%M %p") )
                    lst_c.append(
                        datetime.datetime.strptime(start_time, "%H:%M:%S").strftime(
                            "%I:%M %p"
                        )
                    )
                    # lst_c.append( start_time )
                # myDict[str(date)] = lst_c
                myDict[
                    str(
                        datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime(
                            "%A, %B %d %Y"
                        )
                    )
                ] = lst_c
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
    description = request.args.get("description", type=str)
    customer_id = current_user.CustomerID

    sql_formatted_date = datetime.datetime.strptime(
        selected_date, "%A, %B %d %Y"
    ).strftime("%Y-%m-%d")
    sql_formatted_time = datetime.datetime.strptime(selected_time, "%I:%M %p").strftime(
        "%H:%M:%S"
    )

    start = int(
        datetime.datetime.strptime(str(sql_formatted_time), "%H:%M:%S").strftime("%H")
    )
    end = datetime.datetime.strptime(str(start + 1), "%H").strftime("%H:%M:%S")

    provider = Provider.query.filter_by(ProviderID=provider_id).first()
    provider_name = provider.Name
    provider_industry = provider.Industry
    provider_price = provider.PriceRate

    appointment = ProviderSchedule.query.filter_by(
        ProviderID=provider_id,
        AppointmentDate=sql_formatted_date,
        StartTime=sql_formatted_time,
    ).first()
    appointment.Availability = 1
    db.session.commit()

    if provider_industry == "Nail Technician":
        new_appointment = NailAppointment(
            ProviderID=provider_id,
            CustomerID=customer_id,
            # Type = ,
            # Comment = ,
            StartTime=sql_formatted_time,
            EndTime=end,
            AppDate=sql_formatted_date,
            Status=description,
            Price=provider_price,
        )
        db.session.add(new_appointment)
        db.session.commit()
    else:  # add db commit for petappointment entry
        pass

    return jsonify(
        result_text="You booked an appointment with {} on {} at {}. ".format(
            provider_name,
            selected_date,
            selected_time,
        )
    )


# def get_provider_dropdown_values():
#     today = date.today()
#     d = timedelta(days=21)
#     myDict = {}
#     hours_list = ['12:00 AM', '01:00 AM', '02:00 AM', '03:00 AM', '04:00 AM', '05:00 AM', '06:00 AM', '07:00 AM', '08:00 AM',
#                 '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM',
#                 '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM']

#     for i in range(21):
#         #lst_c = []
#         today = date.today()
#         d = timedelta(i)
#         new_date = today + d
#         #print(new_date)
#         # for hour in hours_list:
#         myDict[str(datetime.datetime.strptime(str(new_date), "%Y-%m-%d").strftime("%A, %B %d %Y"))] = hours_list

#     return myDict


# @views.route("/test", methods=["POST", "GET"])
# def test():

#     # initialize drop down menus

#     class_entry_relations = get_provider_dropdown_values()

#     default_classes = list(class_entry_relations.keys())
#     if class_entry_relations:
#         default_values = class_entry_relations[default_classes[0]]
#     else:
#         default_values = []

#     return render_template(
#         "test.html",
#         all_classes=default_classes,
#         start_time=default_values,
#         end_time=default_values,
#         user=current_user,
#         type=type,
#     )


# @views.route("/_process_provider_schedule")
# def process_provider_schedule():
#     selected_date = request.args.get("selected_date", type=str)
#     start_time = request.args.get("start_time", type=str)
#     end_time = request.args.get("end_time", type=str)
#     provider_id = current_user.ProviderID

#     sql_formatted_date = datetime.datetime.strptime(selected_date, "%A, %B %d %Y").strftime("%Y-%m-%d")
#     sql_formatted_start = datetime.datetime.strptime(start_time, "%I:%M %p").strftime("%H:%M:%S")
#     sql_formatted_end = datetime.datetime.strptime(end_time, "%I:%M %p").strftime("%H:%M:%S")

#     start_hour = int(datetime.datetime.strptime(start_time, "%I:%M %p").strftime("%H"))
#     end_hour = int(datetime.datetime.strptime(end_time, "%I:%M %p").strftime("%H"))


#     for i in range(start_hour, end_hour):
#         start = datetime.datetime.strptime(str(i), "%H").strftime("%H:%M:%S")
#         end = datetime.datetime.strptime(str(i+1), "%H").strftime("%H:%M:%S")
#         print(f" {sql_formatted_date} {start} - {end}")

#     #add db commits to create a new appointment entry
#     #appointment = ProviderSchedule.query.filter_by(ProviderID=provider_id, AppointmentDate = sql_formatted_date, StartTime = sql_formatted_time).first()
#     #appointment.Availability = 1
#     #db.session.commit()

#     return jsonify(
#         random_text="You booked an appointment on {} from {} - {}. ProviderID: {}".format(
#             selected_date, start_time, end_time, provider_id
#         )
#     )
