
from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..extensions import db
from ..models.core import Site, SiteType
from ..models.internet import InternetAccess, InternetAccessType
from ..models.license import SaseLicense, SaseLicenseType
from ..models.equipment import SaseEquipment, SaseEquipmentType
from ..forms.site_assets_forms import InternetAccessForm, SaseLicenseForm, SaseEquipmentForm

site_bp = Blueprint("site_manage", __name__, template_folder="../templates")

def populate_choices(site, form):
    if isinstance(form, InternetAccessForm):
        form.type_id.choices=[(0,"-")]+[(t.id,t.label) for t in InternetAccessType.query.filter_by(client_id=site.client_id)]
    elif isinstance(form, SaseLicenseForm):
        form.type_id.choices=[(0,"-")]+[(t.id,t.label) for t in SaseLicenseType.query.filter_by(client_id=site.client_id)]
    elif isinstance(form, SaseEquipmentForm):
        form.type_id.choices=[(0,"-")]+[(t.id,t.label) for t in SaseEquipmentType.query.filter_by(client_id=site.client_id)]

def equipment_ok(site, new_type_id, exclude_equipment_id=None):
    others=[e for e in site.equipments if e.id!=exclude_equipment_id]
    if len(others)>=2: return False
    if others and new_type_id:
        ref_model = others[0].type.model if others[0].type else None
        new_model = SaseEquipmentType.query.get(new_type_id).model if new_type_id else None
        return ref_model==new_model
    return True

@site_bp.route("/client/<int:client_id>/site/<int:site_id>")
def site_detail(client_id, site_id):
    site=Site.query.get_or_404(site_id)
    return render_template("sites/detail.html", site=site, client=site.client)

# Access, License routes remain same from v13 (copy)...

