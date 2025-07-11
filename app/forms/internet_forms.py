
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class InternetAccessForm(FlaskForm):
    contract_number = StringField("Numéro de contrat", validators=[DataRequired()])
    start_date = DateField("Date de démarrage", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
