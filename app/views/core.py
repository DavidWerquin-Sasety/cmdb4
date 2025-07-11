
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models.core import Client, Site
from ..forms.core_forms import ClientForm, SiteForm

core_bp = Blueprint("core", __name__, template_folder="../templates")

@core_bp.route("/clients")
def list_clients():
    clients = Client.query.all()
    return render_template("clients/list.html", clients=clients)

@core_bp.route("/clients/new", methods=["GET", "POST"])
def create_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data)
        db.session.add(client)
        db.session.commit()
        flash("Client créé", "success")
        return redirect(url_for("core.list_clients"))
    return render_template("clients/form.html", form=form)

@core_bp.route("/client/<int:client_id>/sites")
def list_sites(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template("sites/list.html", client=client)

@core_bp.route("/client/<int:client_id>/site/new", methods=["GET", "POST"])
def create_site(client_id):
    client = Client.query.get_or_404(client_id)
    form = SiteForm()
    if form.validate_on_submit():
        site = Site(
            client=client,
            name=form.name.data,
            code=form.code.data,
            street=form.street.data,
            postal_code=form.postal_code.data,
            city=form.city.data,
            country=form.country.data,
        )
        db.session.add(site)
        db.session.commit()
        flash("Site créé", "success")
        return redirect(url_for("core.list_sites", client_id=client.id))
    return render_template("sites/form.html", form=form, client=client)
