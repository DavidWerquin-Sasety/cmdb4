
from flask import Blueprint, render_template, redirect, url_for, request, flash
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

def render_row(obj):
    if isinstance(obj, InternetAccess):
        return render_template("sites/rows/access_row.html", acc=obj)
    if isinstance(obj, SaseLicense):
        return render_template("sites/rows/license_row.html", lic=obj)
    if isinstance(obj, SaseEquipment):
        return render_template("sites/rows/equipment_row.html", eq=obj)

def equipment_ok(site, new_type_id):
    if len(site.equipments) >= 2:
        flash("Max 2 équipements", "danger")
        return False
    if site.equipments and new_type_id:
        first = site.equipments[0].type.model if site.equipments[0].type else None
        new = SaseEquipmentType.query.get(new_type_id).model if new_type_id else None
        if first and new and first != new:
            flash("Les deux équipements doivent être du même modèle", "danger")
            return False
    return True

COLSPAN = {"access": 4, "license": 3, "equipment": 4}

@site_bp.route("/client/<int:client_id>/site/<int:site_id>")
def site_detail(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    return render_template("sites/detail.html", site=site, client=site.client)

def form_row(key, form, client_id, site_id, obj_id=None):
    if key == "access":
        post = url_for('site_manage.edit_access', client_id=client_id, site_id=site_id, access_id=obj_id) if obj_id else url_for('site_manage.create_access', client_id=client_id, site_id=site_id)
    elif key == "license":
        post = url_for('site_manage.edit_license', client_id=client_id, site_id=site_id, license_id=obj_id) if obj_id else url_for('site_manage.create_license', client_id=client_id, site_id=site_id)
    else:
        post = url_for('site_manage.edit_equipment', client_id=client_id, site_id=site_id, equipment_id=obj_id) if obj_id else url_for('site_manage.create_equipment', client_id=client_id, site_id=site_id)
    cancel = url_for('site_manage.site_detail', client_id=client_id, site_id=site_id)
    return render_template("sites/asset_form_row.html", form=form, colspan=COLSPAN[key], post_url=post, cancel_url=cancel)

# ------------- INTERNET ACCESS -------------
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/new", methods=["GET", "POST"])
def create_access(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = InternetAccessForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        acc = InternetAccess(site=site)
        form.populate_obj(acc)
        acc.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.add(acc)
        db.session.commit()
        return render_row(acc) if request.headers.get("HX-Request") else redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    if request.headers.get("HX-Request"):
        return form_row("access", form, client_id, site_id)
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:access_id>/edit", methods=["GET", "POST"])
def edit_access(client_id, site_id, access_id):
    acc = InternetAccess.query.get_or_404(access_id)
    site = acc.site
    form = InternetAccessForm(obj=acc)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(acc)
        acc.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.commit()
        return render_row(acc) if request.headers.get("HX-Request") else redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    if request.headers.get("HX-Request"):
        return form_row("access", form, client_id, site_id, access_id)
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:access_id>/delete", methods=["POST"])
def delete_access(client_id, site_id, access_id):
    db.session.delete(InternetAccess.query.get_or_404(access_id))
    db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# ------------- LICENSE -------------
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/new", methods=["GET", "POST"])
def create_license(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    if site.licenses:
        flash("Une seule licence par site", "danger")
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    form = SaseLicenseForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        lic = SaseLicense(site=site)
        form.populate_obj(lic)
        lic.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.add(lic)
        db.session.commit()
        return render_row(lic) if request.headers.get("HX-Request") else redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    if request.headers.get("HX-Request"):
        return form_row("license", form, client_id, site_id)
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:license_id>/edit", methods=["GET", "POST"])
def edit_license(client_id, site_id, license_id):
    lic = SaseLicense.query.get_or_404(license_id)
    site = lic.site
    form = SaseLicenseForm(obj=lic)
    populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(lic)
        lic.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.commit()
        return render_row(lic) if request.headers.get("HX-Request") else redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    if request.headers.get("HX-Request"):
        return form_row("license", form, client_id, site_id, license_id)
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:license_id>/delete", methods=["POST"])
def delete_license(client_id, site_id, license_id):
    db.session.delete(SaseLicense.query.get_or_404(license_id))
    db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# ------------- EQUIPMENT -------------
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/new", methods=["GET", "POST"])
def create_equipment(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseEquipmentForm()
    populate_choices(site, form)
    if form.validate_on_submit():
        if not equipment_ok(site, form.type_id.data if form.type_id.data != 0 else None):
            return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
        eq = SaseEquipment(site=site)
        form.populate_obj(eq)
        eq.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.add(eq)
        db.session.commit()
        return render_row(eq) if request.headers.get("HX-Request") else redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    if request.headers.get("HX-Request"):
        return form_row("equipment", form, client_id, site_id)
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:equipment_id>/edit", methods=["GET", "POST"])
def edit_equipment(client_id, site_id, equipment_id):
    eq = SaseEquipment.query.get_or_404(equipment_id)
    site = eq.site
    form = SaseEquipmentForm(obj=eq)
    populate_choices(site, form)
    if form.validate_on_submit():
        if not equipment_ok(site, form.type_id.data if form.type_id.data != 0 else None):
            return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
        form.populate_obj(eq)
        eq.type_id = None if form.type_id.data == 0 else form.type_id.data
        db.session.commit()
        return render_row(eq) if request.headers.get("HX-Request") else redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    if request.headers.get("HX-Request"):
        return form_row("equipment", form, client_id, site_id, equipment_id)
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:equipment_id>/delete", methods=["POST"])
def delete_equipment(client_id, site_id, equipment_id):
    db.session.delete(SaseEquipment.query.get_or_404(equipment_id))
    db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
