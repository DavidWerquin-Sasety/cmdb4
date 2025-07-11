
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ClientForm(FlaskForm):
    name = StringField("Nom du client", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

class SiteForm(FlaskForm):
    name = StringField("Nom du site", validators=[DataRequired()])
    code = StringField("Code", validators=[DataRequired()])
    street = StringField("Rue")
    postal_code = StringField("Code postal")
    city = StringField("Ville")
    country = StringField("Pays")
    site_type_id = SelectField("Type de site", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
