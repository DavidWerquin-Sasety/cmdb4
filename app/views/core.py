
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models.core import Client, Site, SiteType
from ..forms.core_forms import ClientForm, SiteForm

core_bp = Blueprint("core", __name__, template_folder="../templates")

# ---------- Clients ----------
@core_bp.route("/clients")
def list_clients():
    clients = Client.query.all()
    return render_template("clients/list.html", clients=clients)

@core_bp.route("/clients/new", methods=["GET","POST"])
def create_client():
    form = ClientForm()
    if form.validate_on_submit():
        db.session.add(Client(name=form.name.data))
        db.session.commit()
        flash("Client créé","success")
        return redirect(url_for("core.list_clients"))
    return render_template("clients/form.html", form=form)

@core_bp.route("/client/<int:client_id>/edit", methods=["GET","POST"])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.name = form.name.data
        db.session.commit()
        flash("Client mis à jour","success")
        return redirect(url_for("core.list_clients"))
    return render_template("clients/form.html", form=form)

@core_bp.route("/client/<int:client_id>/delete", methods=["GET","POST"])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method=="POST":
        if request.form.get("confirm") == client.name.upper():
            db.session.delete(client); db.session.commit()
            flash("Client supprimé","success")
            return redirect(url_for("core.list_clients"))
        flash("Texte incorrect","danger")
    return render_template("clients/confirm_delete.html", client=client)

# ---------- Sites ----------
@core_bp.route("/client/<int:client_id>/sites")
def list_sites(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template("sites/list.html", client=client)

@core_bp.route("/client/<int:client_id>/site/new", methods=["GET","POST"])
def create_site(client_id):
    client = Client.query.get_or_404(client_id)
    form = SiteForm()
    form.site_type_id.choices = [(t.id,t.label) for t in SiteType.query.filter_by(client_id=client.id)]
    if form.validate_on_submit():
        site = Site(
            client=client,
            name=form.name.data,
            code=form.code.data,
            street=form.street.data,
            postal_code=form.postal_code.data,
            city=form.city.data,
            country=form.country.data
        )
        site.site_type_id = form.site_type_id.data
        db.session.add(site)
        db.session.commit()
        flash("Site créé","success")
        return redirect(url_for("core.list_sites", client_id=client.id))
    return render_template("sites/form.html", form=form, client=client)

@core_bp.route("/client/<int:client_id>/site/<int:site_id>/edit", methods=["GET","POST"])
def edit_site(client_id, site_id):
    client = Client.query.get_or_404(client_id)
    site = Site.query.get_or_404(site_id)
    form = SiteForm(obj=site)
    form.site_type_id.choices = [(t.id,t.label) for t in SiteType.query.filter_by(client_id=client.id)]
    if form.validate_on_submit():
        form.populate_obj(site)
        db.session.commit()
        flash("Site mis à jour","success")
        return redirect(url_for("core.list_sites", client_id=client.id))
    return render_template("sites/form.html", form=form, client=client)

@core_bp.route("/client/<int:client_id>/site/<int:site_id>/delete", methods=["GET","POST"])
def delete_site(client_id, site_id):
    site = Site.query.get_or_404(site_id)
    if request.method=="POST":
        if request.form.get("confirm") == site.name.upper():
            db.session.delete(site); db.session.commit()
            flash("Site supprimé","success")
            return redirect(url_for("core.list_sites", client_id=client_id))
        flash("Confirmation incorrecte","danger")
    return render_template("sites/confirm_delete.html", site=site, client_id=client_id)
