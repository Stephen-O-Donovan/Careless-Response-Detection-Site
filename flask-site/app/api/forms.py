from wtforms import Form
from wtforms_alchemy import model_form_factory


from app.models import *


ModelForm = model_form_factory(Form)


class SurveyForm(ModelForm):
    class Meta:
        model = Survey


class TestForm(ModelForm):
    class Meta:
        model = Test