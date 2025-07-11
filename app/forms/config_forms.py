
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SiteTypeForm(FlaskForm):
    label = StringField("Libellé", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

class InternetTechnologyForm(FlaskForm):
    label = StringField("Libellé", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

class InternetAccessTypeForm(FlaskForm):
    label = StringField("Libellé", validators=[DataRequired()])
    technology_id = SelectField("Technologie", coerce=int, validators=[DataRequired()])
    zone = SelectField("Zone", choices=[(1,"1"),(2,"2"),(3,"3")], coerce=int)
    bandwidth_mbps = IntegerField("Débit (Mbps)", validators=[NumberRange(min=1)])
    quota_gb = IntegerField("Forfait (Go/mois)", validators=[NumberRange(min=0)])
    fas_eur = FloatField("FAS (€ HT)", validators=[NumberRange(min=0)])
    monthly_cost_eur = FloatField("Coût mensuel (€)", validators=[NumberRange(min=0)])
    commitment_months = IntegerField("Engagement (mois)", validators=[NumberRange(min=0)])
    submit = SubmitField("Enregistrer")

class SaseLicenseTypeForm(FlaskForm):
    label = StringField("Libellé", validators=[DataRequired()])
    group = SelectField("Groupe", choices=[(1,"1"),(2,"2")], coerce=int)
    license_type = SelectField("Type", choices=[("Site","Site"),("Pool","Pool")])
    bandwidth_mbps = IntegerField("Débit (Mbps)", validators=[NumberRange(min=1)])
    submit = SubmitField("Enregistrer")

class SaseEquipmentTypeForm(FlaskForm):
    label = StringField("Libellé", validators=[DataRequired()])
    model = SelectField("Modèle", choices=[("X1500","X1500"),("X1600","X1600"),("X1700","X1700")])
    bandwidth_mbps = IntegerField("Débit supporté (Mbps)", validators=[NumberRange(min=1)])
    submit = SubmitField("Enregistrer")
