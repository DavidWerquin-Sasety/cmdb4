
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from ..extensions import db
from ..models.core import Client, SiteType
from ..models.internet import InternetTechnology, InternetAccessType
from ..models.license import SaseLicenseType
from ..models.equipment import SaseEquipmentType
from ..forms.config_forms import (
    SiteTypeForm,
    InternetTechnologyForm,
    InternetAccessTypeForm,
    SaseLicenseTypeForm,
    SaseEquipmentTypeForm,
)

config_bp = Blueprint("config", __name__, template_folder="../templates")

CONFIG_ENTITIES = {
    "site-types": (SiteType, SiteTypeForm, "Types de site"),
    "internet-technologies": (InternetTechnology, InternetTechnologyForm, "Technologies d'accès"),
    "internet-access-types": (InternetAccessType, InternetAccessTypeForm, "Types d'accès internet"),
    "license-types": (SaseLicenseType, SaseLicenseTypeForm, "Types de licence"),
    "equipment-types": (SaseEquipmentType, SaseEquipmentTypeForm, "Types d'équipement"),
}

def get_entity_or_404(entity_key):
    if entity_key not in CONFIG_ENTITIES:
        abort(404)
    return CONFIG_ENTITIES[entity_key]

@config_bp.route("/client/<int:client_id>")
def config_home(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template("config/home.html", client=client, config_entities=CONFIG_ENTITIES)

@config_bp.route("/client/<int:client_id>/<entity_key>")
def list_entities(client_id, entity_key):
    client = Client.query.get_or_404(client_id)
    model, form_cls, title = get_entity_or_404(entity_key)
    items = model.query.filter_by(client_id=client.id).all()
    return render_template("config/list.html", client=client, entity_key=entity_key, title=title, items=items)

@config_bp.route("/client/<int:client_id>/<entity_key>/new", methods=["GET", "POST"])
def create_entity(client_id, entity_key):
    client = Client.query.get_or_404(client_id)
    model, form_cls, title = get_entity_or_404(entity_key)
    form = form_cls()
    if entity_key == "internet-access-types":
        form.technology_id.choices = [(t.id, t.label) for t in InternetTechnology.query.filter_by(client_id=client.id).all()]
    if form.validate_on_submit():
        item = model(client_id=client.id)
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash(f"{title} créé", "success")
        return redirect(url_for('config.list_entities', client_id=client.id, entity_key=entity_key))
    return render_template("config/form.html", form=form, title=f"Créer {title}", client=client)

@config_bp.route("/client/<int:client_id>/<entity_key>/<int:item_id>/edit", methods=["GET", "POST"])
def edit_entity(client_id, entity_key, item_id):
    client = Client.query.get_or_404(client_id)
    model, form_cls, title = get_entity_or_404(entity_key)
    item = model.query.get_or_404(item_id)
    form = form_cls(obj=item)
    if entity_key == "internet-access-types":
        form.technology_id.choices = [(t.id, t.label) for t in InternetTechnology.query.filter_by(client_id=client.id).all()]
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f"{title} mis à jour", "success")
        return redirect(url_for('config.list_entities', client_id=client.id, entity_key=entity_key))
    return render_template("config/form.html", form=form, title=f"Modifier {title}", client=client)

@config_bp.route("/client/<int:client_id>/<entity_key>/<int:item_id>/delete", methods=["POST"])
def delete_entity(client_id, entity_key, item_id):
    model, form_cls, title = get_entity_or_404(entity_key)
    item = model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f"{title} supprimé", "success")
    return redirect(url_for('config.list_entities', client_id=client_id, entity_key=entity_key))
