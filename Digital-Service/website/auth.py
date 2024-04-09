from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from website.forms import SignUpForm, LoginForm

# routes related to authorization
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("Logged In!", "success")
        return redirect(url_for("views.home"))
    else:
        flash("Invalid username or password", "warning")

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
