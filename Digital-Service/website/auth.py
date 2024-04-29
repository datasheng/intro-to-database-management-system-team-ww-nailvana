from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Provider, Customer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from website.forms import SignUpForm, LoginForm, AccountForm

# routes related to authorization
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    form = LoginForm()

    # HEEEEEEEEEEEEEEELP - Any optimizers?
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
    print(current_user.Password)

    if form.validate_on_submit():
        current_user.Username = form.username.data
        current_user.Email = form.email.data
        current_user.Password = generate_password_hash(
            form.new_password.data, method="pbkdf2:sha256"
        )

        db.session.commit()
        flash("Account updated", category="success")
        return redirect(url_for("auth.account"))

    return render_template("account.html", user=current_user, form=form)
