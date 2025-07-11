
from datetime import datetime
from ..extensions import db

class InternetTechnology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    label = db.Column(db.String(32), nullable=False)

class InternetAccessType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    label = db.Column(db.String(64), nullable=False)
    technology_id = db.Column(db.Integer, db.ForeignKey("internet_technology.id"))
    zone = db.Column(db.Integer)
    bandwidth_mbps = db.Column(db.Integer)
    quota_gb = db.Column(db.Integer)
    fas_eur = db.Column(db.Float)
    monthly_cost_eur = db.Column(db.Float)
    commitment_months = db.Column(db.Integer)

    technology = db.relationship("InternetTechnology")

class InternetAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("internet_access_type.id"))
    contract_number = db.Column(db.String(64))
    start_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    type = db.relationship("InternetAccessType", lazy="joined")
