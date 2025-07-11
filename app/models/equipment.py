
from datetime import datetime
from ..extensions import db

class SaseEquipmentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    label = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(16))          # X1500, X1600, X1700
    bandwidth_mbps = db.Column(db.Integer)

class SaseEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("sase_equipment_type.id"))
    serial_number = db.Column(db.String(64))
    start_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
