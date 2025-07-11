
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ClientForm(FlaskForm):
    name = StringField("Nom du client", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

class SiteForm(FlaskForm):
    name = StringField("Nom du site", validators=[DataRequired()])
    code = StringField("Code site", validators=[DataRequired()])
    street = StringField("Rue")
    postal_code = StringField("Code postal")
    city = StringField("Ville")
    country = StringField("Pays")
    submit = SubmitField("Enregistrer")
