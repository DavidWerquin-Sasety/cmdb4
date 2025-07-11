
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models.core import Site
from ..models.internet import InternetAccess, InternetAccessType
from ..models.license import SaseLicense, SaseLicenseType
from ..models.equipment import SaseEquipment, SaseEquipmentType
from ..forms.site_assets_forms import InternetAccessForm, SaseLicenseForm, SaseEquipmentForm

site_bp = Blueprint("site_manage", __name__, template_folder="../templates")

def populate_choices(site, form):
    if isinstance(form, InternetAccessForm):
        form.type_id.choices = [(0, "-")] + [(t.id, t.label) for t in InternetAccessType.query.filter_by(client_id=site.client_id)]
    elif isinstance(form, SaseLicenseForm):
        form.type_id.choices = [(0, "-")] + [(t.id, t.label) for t in SaseLicenseType.query.filter_by(client_id=site.client_id)]
    elif isinstance(form, SaseEquipmentForm):
        form.type_id.choices = [(0, "-")] + [(t.id, t.label) for t in SaseEquipmentType.query.filter_by(client_id=site.client_id)]

def equipment_ok(site, new_type_id, exclude_id=None):
    others = [e for e in site.equipments if e.id != exclude_id]
    if len(others) >= 2:
        return False
    if others and new_type_id:
        ref_model = others[0].type.model if others[0].type else None
        new_model = SaseEquipmentType.query.get(new_type_id).model if new_type_id else None
        return ref_model == new_model
    return True

@site_bp.route("/client/<int:client_id>/site/<int:site_id>")
def site_detail(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    return render_template("sites/detail.html", site=site, client=site.client)

# ------- INTERNET ACCESS -------
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/new", methods=["GET","POST"])
def create_access(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    if len(site.accesses) >= 3:
        flash("Limite de 3 accès atteinte", "danger")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    form = InternetAccessForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        acc = InternetAccess(site=site)
        form.populate_obj(acc)
        acc.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.add(acc)
        db.session.commit()
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_page.html", form=form, title="Nouvel accès internet", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:access_id>/edit", methods=["GET","POST"])
def edit_access(client_id, site_id, access_id):
    acc = InternetAccess.query.get_or_404(access_id)
    site = acc.site
    form = InternetAccessForm(obj=acc)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(acc)
        acc.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.commit()
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_page.html", form=form, title="Modifier accès internet", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:access_id>/delete", methods=["POST"])
def delete_access(client_id, site_id, access_id):
    db.session.delete(InternetAccess.query.get_or_404(access_id))
    db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# ------- LICENSE -------
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/new", methods=["GET","POST"])
def create_license(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    if site.licenses:
        flash("Une seule licence autorisée", "danger")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    form = SaseLicenseForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        lic = SaseLicense(site=site)
        form.populate_obj(lic)
        lic.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.add(lic)
        db.session.commit()
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_page.html", form=form, title="Nouvelle licence SASE", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:license_id>/edit", methods=["GET","POST"])
def edit_license(client_id, site_id, license_id):
    lic = SaseLicense.query.get_or_404(license_id)
    site = lic.site
    form = SaseLicenseForm(obj=lic)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(lic)
        lic.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.commit()
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_page.html", form=form, title="Modifier licence SASE", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:license_id>/delete", methods=["POST"])
def delete_license(client_id, site_id, license_id):
    db.session.delete(SaseLicense.query.get_or_404(license_id))
    db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# ------- EQUIPMENT -------
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/new", methods=["GET","POST"])
def create_equipment(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseEquipmentForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        if not equipment_ok(site, form.type_id.data if form.type_id.data!=0 else None):
            flash("Deux équipements max et même modèle", "danger")
            return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
        eq = SaseEquipment(site=site)
        form.populate_obj(eq)
        eq.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.add(eq)
        db.session.commit()
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_page.html", form=form, title="Nouvel équipement SASE", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:equipment_id>/edit", methods=["GET","POST"])
def edit_equipment(client_id, site_id, equipment_id):
    eq = SaseEquipment.query.get_or_404(equipment_id)
    site = eq.site
    form = SaseEquipmentForm(obj=eq)
    populate_choices(site, form)
    if form.validate_on_submit():
        if not equipment_ok(site, form.type_id.data if form.type_id.data!=0 else None, exclude_id=equipment_id):
            flash("Les deux équipements doivent rester du même modèle", "danger")
            return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
        form.populate_obj(eq)
        eq.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.commit()
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_page.html", form=form, title="Modifier équipement SASE", site=site, client=site.client)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:equipment_id>/delete", methods=["POST"])
def delete_equipment(client_id, site_id, equipment_id):
    db.session.delete(SaseEquipment.query.get_or_404(equipment_id))
    db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
