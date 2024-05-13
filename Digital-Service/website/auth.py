from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify 
from .models import Provider, Customer, ProviderSchedule
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import datetime
from datetime import timedelta, date
import calendar
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from website.forms import SignUpForm, LoginForm, AccountForm, ProviderForm

# routes related to authorization
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    form = LoginForm()

    if form.validate_on_submit():
        provider = Provider.query.filter_by(Email=form.email.data).first()
        customer = Customer.query.filter_by(Email=form.email.data).first()
        print(provider, customer)

        if provider and check_password_hash(provider.Password, form.password.data):
            login_user(provider, remember=True)
            flash("Logged In!", "success")
            return redirect(url_for("views.home"))

        elif customer and check_password_hash(customer.Password, form.password.data):
            login_user(customer, remember=True)
            flash("Logged In!", "success")
            return redirect(url_for("views.home"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html", form=form, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    form = SignUpForm()

    if form.validate_on_submit():
        if form.user_role.data == "Provider":
            new_user = Provider(
                Email=form.email.data,
                Name=form.name.data,
                Username=form.username.data,
                Password=generate_password_hash(
                    form.password.data, method="pbkdf2:sha256"
                ),
            )
        else:
            new_user = Customer(
                Email=form.email.data,
                Name=form.name.data,
                Username=form.username.data,
                Password=generate_password_hash(
                    form.password.data, method="pbkdf2:sha256"
                ),
            )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash("Account created.", category="success")
        return redirect(url_for("views.home"))
    return render_template("signup.html", user=current_user, form=form)


# current_user table
def current_user_logged_in():
    provider = Provider.query.filter_by(Email=current_user.Email).first()
    customer = Customer.query.filter_by(Email=current_user.Email).first()
    if provider is not None:
        print(current_user.Email)
        return "provider"
    elif customer is not None:
        print(current_user.Email)
        return "customer"
    else:
        return None


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountForm()
    type = current_user_logged_in()
    print(current_user.Password)

    if form.validate_on_submit():
        current_user.Username = form.username.data
        current_user.Email = form.email.data
        current_user.Number = form.number.data
        if form.new_password.data:
            current_user.Password = generate_password_hash(
                form.new_password.data, method="pbkdf2:sha256"
            )

        db.session.commit()
        flash("Account updated", category="success")
        return redirect(url_for("auth.account"))

    return render_template("account.html", user=current_user, form=form, type=type)


@auth.route("/provider_profile", methods=["GET", "POST"])
@login_required
def provider_profile():
    type = current_user_logged_in()
    form = ProviderForm()

    # number, address --> account route?
    if form.validate_on_submit():
        current_user.Industry = form.industry.data
        current_user.Address = form.address.data
        current_user.Company = form.company.data
        current_user.Specialization = form.specialization.data
        current_user.PriceRate = form.price_rate.data

        db.session.commit()
        flash("Profile updated", category="success")
        return redirect(url_for("auth.provider_profile"))
    
    class_entry_relations = get_provider_dropdown_values()

    default_classes = list(class_entry_relations.keys())
    if class_entry_relations:
        default_values = class_entry_relations[default_classes[0]]
    else:
        default_values = []

    return render_template(
        "providerprofile.html",
        form = form,
        all_classes=default_classes,
        start_time=default_values,
        end_time=default_values,
        user=current_user,
        type=type,
    )

    return render_template(
        "providerprofile.html", user=current_user, form=form, type=type
    )



def get_provider_dropdown_values():
    today = date.today()
    myDict = {}
    hours_list = ['12:00 AM', '01:00 AM', '02:00 AM', '03:00 AM', '04:00 AM', '05:00 AM', '06:00 AM', '07:00 AM', '08:00 AM',
                '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM', 
                '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM']

    for i in range(31):
        #lst_c = []
        today = date.today()
        d = timedelta(i)
        new_date = today + d
        #print(new_date)
        # for hour in hours_list:
        myDict[str(datetime.datetime.strptime(str(new_date), "%Y-%m-%d").strftime("%A, %B %d %Y"))] = hours_list

    return myDict 


@auth.route("/_process_provider_schedule")
def process_provider_schedule():
    selected_date = request.args.get("selected_date", type=str)
    start_time = request.args.get("start_time", type=str)
    end_time = request.args.get("end_time", type=str)
    provider_id = current_user.ProviderID

    sql_formatted_date = datetime.datetime.strptime(selected_date, "%A, %B %d %Y").strftime("%Y-%m-%d")

    start_hour = int(datetime.datetime.strptime(start_time, "%I:%M %p").strftime("%H"))
    end_hour = int(datetime.datetime.strptime(end_time, "%I:%M %p").strftime("%H"))

    for i in range(start_hour, end_hour):
        start = datetime.datetime.strptime(str(i), "%H").strftime("%H:%M:%S")
        end = datetime.datetime.strptime(str(i+1), "%H").strftime("%H:%M:%S")
        new_time_slot = ProviderSchedule(
            ProviderID = provider_id,
            StartTime = start,
            EndTime = end,
            AppointmentDate = sql_formatted_date
        )
        db.session.add(new_time_slot)
        db.session.commit()

    return jsonify(
        random_text="You added {}, from {} - {}.".format(
            selected_date, start_time, end_time, 
        )
    )