
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import Optional

class InternetAccessForm(FlaskForm):
    type_id = SelectField("Type d'accès", coerce=int, validators=[Optional()])
    contract_number = StringField("Numéro de contrat", validators=[Optional()])
    start_date = DateField("Date de démarrage", validators=[Optional()])
    submit = SubmitField("Enregistrer")

class SaseLicenseForm(FlaskForm):
    type_id = SelectField("Type de licence", coerce=int, validators=[Optional()])
    start_date = DateField("Date de démarrage", validators=[Optional()])
    submit = SubmitField("Enregistrer")

class SaseEquipmentForm(FlaskForm):
    type_id = SelectField("Type d'équipement", coerce=int, validators=[Optional()])
    serial_number = StringField("Numéro de série", validators=[Optional()])
    start_date = DateField("Date de démarrage", validators=[Optional()])
    submit = SubmitField("Enregistrer")
