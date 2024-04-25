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

    # TODO: Custom validators
    # user = User.query.filter_by(email=email).first()
    # if user:
    #     flash("Email already exists", category="error")
    def validate_email(self, email):
        provider = Provider.query.filter_by(Email=email.data).first()
        customer = Customer.query.filter_by(Email=email.data).first()

        if provider or customer:
            raise ValidationError(
                "There is an account with that email. Please choose another or log in"
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")


# TODO: Review form
