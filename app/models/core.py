
from datetime import datetime
from ..extensions import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    sites = db.relationship("Site", backref="client", cascade="all, delete-orphan")

class SiteType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    label = db.Column(db.String(64), nullable=False)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)

    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), nullable=False)
    street = db.Column(db.String(128))
    postal_code = db.Column(db.String(16))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))

    site_type_id = db.Column(db.Integer, db.ForeignKey("site_type.id"))
    site_type = db.relationship("SiteType", lazy="joined")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Child collections
    accesses = db.relationship("InternetAccess", backref="site", cascade="all, delete-orphan")
    licenses = db.relationship("SaseLicense", backref="site", cascade="all, delete-orphan")
    equipments = db.relationship("SaseEquipment", backref="site", cascade="all, delete-orphan")
