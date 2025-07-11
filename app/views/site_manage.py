
from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..extensions import db
from ..models.core import Site
from ..models.internet import InternetAccess, InternetAccessType
from ..models.license import SaseLicense, SaseLicenseType
from ..models.equipment import SaseEquipment, SaseEquipmentType
from ..forms.site_assets_forms import InternetAccessForm, SaseLicenseForm, SaseEquipmentForm

site_bp = Blueprint("site_manage", __name__, template_folder="../templates")

# helpers
def populate_choices(site, form):
    if isinstance(form, InternetAccessForm):
        form.type_id.choices = [(0,"-")] + [(t.id, t.label) for t in InternetAccessType.query.filter_by(client_id=site.client_id)]
    elif isinstance(form, SaseLicenseForm):
        form.type_id.choices = [(0,"-")] + [(t.id, t.label) for t in SaseLicenseType.query.filter_by(client_id=site.client_id)]
    elif isinstance(form, SaseEquipmentForm):
        form.type_id.choices = [(0,"-")] + [(t.id, t.label) for t in SaseEquipmentType.query.filter_by(client_id=site.client_id)]

def render_row(obj):
    if isinstance(obj, InternetAccess):
        return render_template("sites/rows/access_row.html", acc=obj)
    if isinstance(obj, SaseLicense):
        return render_template("sites/rows/license_row.html", lic=obj)
    if isinstance(obj, SaseEquipment):
        return render_template("sites/rows/equipment_row.html", eq=obj)
    return ""

def equipment_ok(site, new_type_id):
    if len(site.equipments) >= 2:
        flash("Max 2 équipements.","danger"); return False
    if site.equipments and new_type_id:
        model0 = site.equipments[0].type.model if site.equipments[0].type else None
        model_new = SaseEquipmentType.query.get(new_type_id).model if new_type_id else None
        if model0 and model_new and model0 != model_new:
            flash("Les deux équipements doivent être du même modèle.","danger"); return False
    return True

# routes
@site_bp.route("/client/<int:client_id>/site/<int:site_id>")
def site_detail(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    return render_template("sites/detail.html", site=site, client=site.client)

# Access CRUD
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/new", methods=["GET","POST"])
def create_access(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    if len(site.accesses) >= 3:
        flash("Max 3 accès","danger"); return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    form = InternetAccessForm(); populate_choices(site, form)
    if form.validate_on_submit():
        a = InternetAccess(site=site); form.populate_obj(a)
        if form.type_id.data==0: a.type_id=None
        db.session.add(a); db.session.commit()
        if request.headers.get("HX-Request"): return render_row(a)
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_inline.html", form=form)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:aid>/edit", methods=["GET","POST"])
def edit_access(client_id, site_id, aid):
    a = InternetAccess.query.get_or_404(aid); site=a.site
    form = InternetAccessForm(obj=a); populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(a); a.type_id = None if form.type_id.data==0 else form.type_id.data
        db.session.commit()
        if request.headers.get("HX-Request"): return render_row(a)
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_inline.html", form=form)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/access/<int:aid>/delete", methods=["POST"])
def delete_access(client_id, site_id, aid):
    db.session.delete(InternetAccess.query.get_or_404(aid)); db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# License CRUD
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/new", methods=["GET","POST"])
def create_license(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    if site.licenses:
        flash("Une seule licence.","danger"); return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    form = SaseLicenseForm(); populate_choices(site, form)
    if form.validate_on_submit():
        l = SaseLicense(site=site); form.populate_obj(l)
        if form.type_id.data==0: l.type_id=None
        db.session.add(l); db.session.commit()
        if request.headers.get("HX-Request"): return render_row(l)
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_inline.html", form=form)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:lid>/edit", methods=["GET","POST"])
def edit_license(client_id, site_id, lid):
    l = SaseLicense.query.get_or_404(lid); site=l.site
    form = SaseLicenseForm(obj=l); populate_choices(site, form)
    if form.validate_on_submit():
        form.populate_obj(l); l.type_id=None if form.type_id.data==0 else form.type_id.data
        db.session.commit()
        if request.headers.get("HX-Request"): return render_row(l)
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_inline.html", form=form)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/license/<int:lid>/delete", methods=["POST"])
def delete_license(client_id, site_id, lid):
    db.session.delete(SaseLicense.query.get_or_404(lid)); db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))

# Equipment CRUD
@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/new", methods=["GET","POST"])
def create_equipment(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    form = SaseEquipmentForm(); populate_choices(site, form)
    if form.validate_on_submit():
        if not equipment_ok(site, form.type_id.data if form.type_id.data!=0 else None):
            return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
        e = SaseEquipment(site=site); form.populate_obj(e)
        if form.type_id.data==0: e.type_id=None
        db.session.add(e); db.session.commit()
        if request.headers.get("HX-Request"): return render_row(e)
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_inline.html", form=form)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:eqid>/edit", methods=["GET","POST"])
def edit_equipment(client_id, site_id, eqid):
    e = SaseEquipment.query.get_or_404(eqid); site=e.site
    form = SaseEquipmentForm(obj=e); populate_choices(site, form)
    if form.validate_on_submit():
        if not equipment_ok(site, form.type_id.data if form.type_id.data!=0 else None):
            return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
        form.populate_obj(e); e.type_id=None if form.type_id.data==0 else form.type_id.data
        db.session.commit()
        if request.headers.get("HX-Request"): return render_row(e)
        return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
    return render_template("sites/asset_form_inline.html", form=form)

@site_bp.route("/client/<int:client_id>/site/<int:site_id>/equipment/<int:eqid>/delete", methods=["POST"])
def delete_equipment(client_id, site_id, eqid):
    db.session.delete(SaseEquipment.query.get_or_404(eqid)); db.session.commit()
    return redirect(url_for('site_manage.site_detail', client_id=client_id, site_id=site_id))
