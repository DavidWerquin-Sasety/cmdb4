
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models.core import Site
from ..models.internet import InternetAccess, InternetAccessType
from ..models.license import SaseLicense, SaseLicenseType
from ..models.equipment import SaseEquipment, SaseEquipmentType
from ..forms.site_assets_forms import InternetAccessForm, SaseLicenseForm, SaseEquipmentForm

site_bp = Blueprint("site_manage", __name__, template_folder="../templates")

def populate_choices(site, form):
    form.type_id.choices = []
    if isinstance(form, InternetAccessForm):
        form.type_id.choices = [(0, "-")] + [(t.id, t.label) for t in InternetAccessType.query.filter_by(client_id=site.client_id).all()]
    elif isinstance(form, SaseLicenseForm):
        form.type_id.choices = [(0, "-")] + [(t.id, t.label) for t in SaseLicenseType.query.filter_by(client_id=site.client_id).all()]
    elif isinstance(form, SaseEquipmentForm):
        form.type_id.choices = [(0, "-")] + [(t.id, t.label) for t in SaseEquipmentType.query.filter_by(client_id=site.client_id).all()]

@site_bp.route("/client/<int:client_id>/site/<int:site_id>")
def site_detail(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    return render_template("sites/detail.html", site=site, client=site.client)

# INTERNET ACCESS CRUD
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/new", methods=["GET", "POST"])
def create_access(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = InternetAccessForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        obj = InternetAccess(site=site)
        form.populate_obj(obj)
        if form.type_id.data == 0:
            obj.type_id = None
        db.session.add(obj)
        db.session.commit()
        flash("Accès internet ajouté", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Nouvel accès internet", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:access_id>/edit", methods=["GET", "POST"])
def edit_access(client_id, site_id, access_id):
    site = Site.query.get_or_404(site_id)
    acc = InternetAccess.query.get_or_404(access_id)
    form = InternetAccessForm(obj=acc)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(acc)
        if form.type_id.data == 0:
            acc.type_id = None
        db.session.commit()
        flash("Accès internet modifié", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Modifier accès internet", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:access_id>/delete", methods=["POST"])
def delete_access(client_id, site_id, access_id):
    acc = InternetAccess.query.get_or_404(access_id)
    db.session.delete(acc)
    db.session.commit()
    flash("Accès internet supprimé", "success")
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# LICENSE CRUD
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/new", methods=["GET", "POST"])
def create_license(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseLicenseForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        obj = SaseLicense(site=site)
        form.populate_obj(obj)
        if form.type_id.data == 0:
            obj.type_id = None
        db.session.add(obj)
        db.session.commit()
        flash("Licence SASE ajoutée", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Nouvelle licence SASE", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:lic_id>/edit", methods=["GET", "POST"])
def edit_license(client_id, site_id, lic_id):
    site = Site.query.get_or_404(site_id)
    lic = SaseLicense.query.get_or_404(lic_id)
    form = SaseLicenseForm(obj=lic)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(lic)
        if form.type_id.data == 0:
            lic.type_id = None
        db.session.commit()
        flash("Licence SASE modifiée", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Modifier licence SASE", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:lic_id>/delete", methods=["POST"])
def delete_license(client_id, site_id, lic_id):
    lic = SaseLicense.query.get_or_404(lic_id)
    db.session.delete(lic)
    db.session.commit()
    flash("Licence SASE supprimée", "success")
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# EQUIPMENT CRUD
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/new", methods=["GET", "POST"])
def create_equipment(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseEquipmentForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        obj = SaseEquipment(site=site)
        form.populate_obj(obj)
        if form.type_id.data == 0:
            obj.type_id = None
        db.session.add(obj)
        db.session.commit()
        flash("Équipement SASE ajouté", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Nouvel équipement SASE", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:eq_id>/edit", methods=["GET", "POST"])
def edit_equipment(client_id, site_id, eq_id):
    site = Site.query.get_or_404(site_id)
    eq = SaseEquipment.query.get_or_404(eq_id)
    form = SaseEquipmentForm(obj=eq)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(eq)
        if form.type_id.data == 0:
            eq.type_id = None
        db.session.commit()
        flash("Équipement SASE modifié", "success")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form.html", form=form, title="Modifier équipement SASE", site=site)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:eq_id>/delete", methods=["POST"])
def delete_equipment(client_id, site_id, eq_id):
    eq = SaseEquipment.query.get_or_404(eq_id)
    db.session.delete(eq)
    db.session.commit()
    flash("Équipement SASE supprimé", "success")
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
