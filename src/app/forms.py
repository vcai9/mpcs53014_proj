import requests
from app import app
from flask import request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BookForm(FlaskForm):
    gr_id = StringField('Goodreads ID', validators=[DataRequired()])
    num_books = IntegerField('How many books?', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Get recommendations!')

    def validate(self, *args, **kwargs):
        super(BookForm, self).validate(*args, **kwargs)
        id_input = self.gr_id.raw_data[0]
        r = requests.get(app.config['GOODREADS_URL'].format(app.config['GOODREADS_API_KEY'], id_input))
        if r.status_code == 404:
            self.gr_id.errors.append("Invalid Goodreads ID")
            return False
        return True