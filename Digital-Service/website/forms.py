from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
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
from datetime import datetime
from werkzeug.security import check_password_hash


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
    new_password = PasswordField("Enter New Password", validators=[Optional()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("new_password"), Optional()]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    number = StringField(
        "Phone Number", validators=[Optional(), Length(min=10, max=14)]
    )

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


class ProviderForm(FlaskForm):
    industry = StringField("Industry:", validators=[Length(max=64)])
    address = StringField("Address:", validators=[Length(max=255)])
    company = StringField("Company:", validators=[Length(max=64)])
    specialization = StringField("Specialization:", validators=[Length(max=64)])
    price_rate = IntegerField("Price Rate:")
    submit = SubmitField("Update")


class BookingForm(FlaskForm):
    name = StringField("Full Name:", validators=[DataRequired()])
    """ description = TextAreaField("Description:")
     type = SelectField("Select Appointment Type:",
        choices=[
            ("", "Select"),
            ("consult", "Consultation"),
            ("mani", "Manicure")
            ("treat", "Treatment"),
            ("other", "Other")]) """
    start_time = SelectField(
        "Select Appointment Time",
        choices=[
            ("09:00", "9:00 AM"),
            ("10:00", "10:00 AM"),
            ("11:00", "11:00 AM"),
            ("12:00", "12:00 PM"),
            ("13:00", "1:00 PM"),
            ("14:00", "2:00 PM"),
            ("15:00", "3:00 PM"),
            ("16:00", "4:00 PM"),
            ("17:00", "5:00 PM"),
            ("18:00", "6:00 PM"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Book Appointment")

    def get_datetime(self, date):
        selected_time = self.start_time.data
        appointment_datetime = datetime.strptime(
            f"{date} {selected_time}", "%Y-%m-%d %I:%M"
        )
        return appointment_datetime
