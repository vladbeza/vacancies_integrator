from flask_wtf import FlaskForm
from config import languages
from integrator.models import City
from wtforms import RadioField, TextAreaField, BooleanField, SelectField, \
    SubmitField, IntegerField


class FilterJobsForm(FlaskForm):
    city = SelectField('City')
    language = SelectField(
        'Language', choices=[(l, l) for l in languages])
    automation_only = BooleanField('Automation')
    remote_only = BooleanField('Remote')
    known_salary = BooleanField('Known salary')
    salary_more = IntegerField('Salary more than', default=0)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(FilterJobsForm, self).__init__(*args, **kwargs)
        self.city.choices = [(str(city.id), city.name)
                             for city in City.query.all()]
        self.city.choices.append(("Any", "Any"))
