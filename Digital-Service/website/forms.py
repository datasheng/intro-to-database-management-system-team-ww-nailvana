from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Optional,
    ValidationError,
)
from .models import Provider, Customer
from werkzeug.security import check_password_hash, generate_password_hash


class SignUpForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=32)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    user_role = SelectField(
        "Account Type",
        choices=[
            ("", "Select an account type"),
            ("Provider", "Service Provider"),
            ("Customer", "Customer"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        provider = Provider.query.filter_by(Email=email.data).first()
        customer = Customer.query.filter_by(Email=email.data).first()

        if provider or customer:
            raise ValidationError(
                "There is an account with that email. Please choose another or log in"
            )

    def validate_username(self, username):
        provider = Provider.query.filter_by(Username=username.data).first()
        customer = Customer.query.filter_by(Username=username.data).first()

        if provider or customer:
            raise ValidationError(
                "There is an account with that username. Please choose another or log in"
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")


class AccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Enter Old Password", validators=[DataRequired()])
    new_password = PasswordField("Enter New Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.Username:
            provider = Provider.query.filter_by(Username=username.data).first()
            customer = Customer.query.filter_by(Username=username.data).first()

            if provider or customer:
                raise ValidationError(
                    "There is an account with that username. Please choose another or log in"
                )

    def validate_email(self, email):
        if email.data != current_user.Email:
            provider = Provider.query.filter_by(Email=email.data).first()
            customer = Customer.query.filter_by(Email=email.data).first()

            if provider or customer:
                raise ValidationError(
                    "There is an account with that email. Please choose another or log in"
                )

    def validate_password(self, password):
        if not check_password_hash(current_user.Password, password.data):
            raise ValidationError(
                "Old password is incorrect. Please enter your current password"
            )


# TODO: Review form
