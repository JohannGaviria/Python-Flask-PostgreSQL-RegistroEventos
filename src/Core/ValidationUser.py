from src.Models.Users import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class UsersForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(max=100, message="Name must be at most 100 characters long")
    ])
    identification_document = StringField('Identification Document', validators=[
        DataRequired(message="Identification Document is required"),
        Length(min=10, message="Identification Document must be at least 10 characters long"),
        Length(max=20, message="Identification Document must be at most 20 characters long")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(),
        Length(max=100, message="Email must be at most 100 characters long")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        Length(max=100, message="Password must be at most 100 characters long")
    ])
    phone = StringField('Phone', validators=[
        DataRequired(message="Phone is required"),
        Length(max=20, message="phone must be at most 20 characters long")
    ])

    def validate_identification_document(self, identification_document):
        user = User.query.filter_by(identification_document=identification_document.data).first()
        if user:
            raise ValidationError('This identification document is already registered.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('This phone number is already registered.')