from extensions import db
from datetime import datetime

class OvertimeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), nullable=False)
    time_logged = db.Column(db.String(20), nullable=False)  # Stored as a string for simplicity
    client_name = db.Column(db.String(100), nullable=False)
    manager_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # New field: pending, approved, denied

    def to_dict(self):
        return {
            "ticket_number": self.ticket_number,
            "time_logged": self.time_logged,
            "client_name": self.client_name,
            "manager_name": self.manager_name,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "status": self.status
        }
