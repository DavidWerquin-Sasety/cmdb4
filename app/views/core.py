
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models.core import Client, Site
from ..forms.core_forms import ClientForm, SiteForm

core_bp = Blueprint("core", __name__, template_folder="../templates")

# ----- Client CRUD -----
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
        flash("Client créé", "success")
        return redirect(url_for('core.list_clients'))
    return render_template("clients/form.html", form=form)

@core_bp.route("/client/<int:cid>/edit", methods=["GET","POST"])
def edit_client(cid):
    client = Client.query.get_or_404(cid)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.name = form.name.data
        db.session.commit()
        flash("Client mis à jour","success")
        return redirect(url_for('core.list_clients'))
    return render_template("clients/form.html", form=form)

@core_bp.route("/client/<int:cid>/delete", methods=["GET","POST"])
def delete_client(cid):
    client = Client.query.get_or_404(cid)
    if request.method=="POST":
        if request.form.get("confirm") == client.name.upper():
            db.session.delete(client); db.session.commit()
            flash("Client supprimé","success")
            return redirect(url_for('core.list_clients'))
        flash("Texte de confirmation incorrect.","danger")
        return redirect(url_for('core.delete_client', cid=cid))
    return render_template("clients/confirm_delete.html", client=client)

# ----- Sites -----
@core_bp.route("/client/<int:cid>/sites")
def list_sites(cid):
    client = Client.query.get_or_404(cid)
    return render_template("sites/list.html", client=client)

@core_bp.route("/client/<int:cid>/site/new", methods=["GET","POST"])
def create_site(cid):
    client = Client.query.get_or_404(cid)
    form = SiteForm()
    if form.validate_on_submit():
        site = Site(client=client, name=form.name.data, code=form.code.data,
                    street=form.street.data, postal_code=form.postal_code.data,
                    city=form.city.data, country=form.country.data)
        db.session.add(site); db.session.commit()
        flash("Site créé","success")
        return redirect(url_for('core.list_sites', cid=cid))
    return render_template("sites/form.html", form=form, client=client)
