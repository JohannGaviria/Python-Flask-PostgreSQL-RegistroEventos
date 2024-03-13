from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class EventsForm(FlaskForm):
    creator_id = IntegerField('Creator ID', validators=[
        DataRequired(message="Ccreator ID is required"),
        NumberRange(min=1, message="Creator ID must be a positive integer"),
    ])
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(max=100, message="Name must be at most 100 characters long")
    ])
    start_date = DateTimeLocalField('Start  Date', validators=[
        DataRequired(message="Start Date is required"),
    ])
    end_date = DateTimeLocalField('End  Date', validators=[
        DataRequired(message="End Date is required"),
    ])
    location = StringField('Location', validators=[
        DataRequired('Location is required'),
        Length(max=255, message="Location must be at most 255 characters long")
    ])

    def validate_end_date(form, field):
        if form.start_date.data and field.data:
            if field.data <= form.start_date.data:
                raise ValidationError('End Date must be after Start Date.')