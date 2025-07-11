
from flask import Blueprint, render_template, redirect, url_for, flash
from ..extensions import db
from ..models.core import Site
from ..models.internet import InternetAccess, InternetAccessType
from ..models.license import SaseLicense, SaseLicenseType
from ..models.equipment import SaseEquipment, SaseEquipmentType
from ..forms.site_assets_forms import InternetAccessForm, SaseLicenseForm, SaseEquipmentForm

site_bp = Blueprint("site_manage", __name__, template_folder="../templates")

@site_bp.route("/client/<int:client_id>/site/<int:site_id>")
def site_detail(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    return render_template("sites/detail.html", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/new", methods=["GET", "POST"])
def create_access(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = InternetAccessForm()
    form.type_id.choices = [(t.id, t.label) for t in InternetAccessType.query.filter_by(client_id=site.client_id).all()]
    if form.validate_on_submit():
        obj = InternetAccess(site=site)
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()
        flash("Accès internet ajouté", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Nouvel accès internet", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/new", methods=["GET", "POST"])
def create_license(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseLicenseForm()
    form.type_id.choices = [(t.id, t.label) for t in SaseLicenseType.query.filter_by(client_id=site.client_id).all()]
    if form.validate_on_submit():
        obj = SaseLicense(site=site)
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()
        flash("Licence SASE ajoutée", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Nouvelle licence SASE", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/new", methods=["GET", "POST"])
def create_equipment(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseEquipmentForm()
    form.type_id.choices = [(t.id, t.label) for t in SaseEquipmentType.query.filter_by(client_id=site.client_id).all()]
    if form.validate_on_submit():
        obj = SaseEquipment(site=site)
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()
        flash("Équipement SASE ajouté", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Nouvel équipement SASE", site=site)
