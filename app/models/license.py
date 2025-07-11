
from datetime import datetime
from ..extensions import db

class SaseLicenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    label = db.Column(db.String(64), nullable=False)
    group = db.Column(db.Integer)  # 1 or 2
    license_type = db.Column(db.String(16))  # Site or Pool
    bandwidth_mbps = db.Column(db.Integer)

class SaseLicense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("sase_license_type.id"))
    start_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
