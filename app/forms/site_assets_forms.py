
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class InternetAccessForm(FlaskForm):
    type_id = SelectField("Type d'accès", coerce=int, validators=[DataRequired()])
    contract_number = StringField("Numéro de contrat", validators=[DataRequired()])
    start_date = DateField("Date de démarrage", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

class SaseLicenseForm(FlaskForm):
    type_id = SelectField("Type de licence", coerce=int, validators=[DataRequired()])
    start_date = DateField("Date de démarrage", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

class SaseEquipmentForm(FlaskForm):
    type_id = SelectField("Type d'équipement", coerce=int, validators=[DataRequired()])
    serial_number = StringField("Numéro de série", validators=[DataRequired()])
    start_date = DateField("Date de démarrage", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
