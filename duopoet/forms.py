from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField, IntegerField
from wtforms.fields import BooleanField, StringField, SubmitField

class AddFragmentsForm(FlaskForm):
	fragments = TextAreaField('Fragments')
	submit = SubmitField('Add Fragments')

class ApproveFragmentsForm(FlaskForm):
    fragment_id = IntegerField()
    fragment_text = StringField('Fragment')
    submit = SubmitField('Approve Fragment')
    delete = SubmitField('Delete Fragment')