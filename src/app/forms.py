from flask import request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BookForm(FlaskForm):
    gr_id = StringField('Goodreads ID', validators=[DataRequired()])
    num_books = IntegerField('How many books?', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Get recommendations!')
