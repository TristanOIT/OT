from app import db
from datetime import datetime

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(100), unique=True, nullable=False)
    hardware_status = db.Column(db.String(50), nullable=False)  # e.g., "In Storage", "Deployed", "In Transport"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
