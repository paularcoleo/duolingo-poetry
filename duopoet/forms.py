from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField
from wtforms.fields import BooleanField, StringField, SubmitField

class AddFragmentsForm(FlaskForm):
	fragments = TextAreaField('Fragments')
	submit = SubmitField('Add Fragments')