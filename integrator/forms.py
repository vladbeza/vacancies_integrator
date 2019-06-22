from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms.widgets import ListWidget, CheckboxInput

from config import languages, skills
from integrator.models import City
from wtforms import RadioField, TextAreaField, BooleanField, SelectField, \
    SubmitField, IntegerField, SelectMultipleField, DateField, DateTimeField


class FilterJobsForm(FlaskForm):
    city = SelectField('City')
    language = SelectField(
        'Language', choices=[(l, l) for l in languages])
    automation_only = BooleanField('Automation')
    remote_only = BooleanField('Remote')
    known_salary = BooleanField('Known salary')
    use_dou_stats = BooleanField('Use Dou Source', default="checked")
    use_djinni = BooleanField('Use Djinni Source', default="checked")
    salary_more = IntegerField('Salary more than', default=0)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(FilterJobsForm, self).__init__(*args, **kwargs)
        self.city.choices = [(str(city.id), city.name)
                             for city in City.query.all()]
        self.city.choices.append(("Any", "Any"))


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SkillsForm(FlaskForm):

    skills_list = MultiCheckboxField("Skills", choices=[(s, s) for s in skills])
    from_date = DateTimeField('Start Date',
                          format='%m/%d/%Y',
                          default=datetime.today() - timedelta(days=30))
    to_date = DateTimeField('End Date',
                        format='%m/%d/%Y',
                        default=datetime.today())
    submit = SubmitField('Submit')
