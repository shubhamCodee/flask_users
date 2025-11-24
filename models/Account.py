from config.database import db
from datetime import datetime
import uuid

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    assigned_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    team_id = db.Column(db.String(36), nullable=True)
    helpdesk_user_team_id = db.Column(db.String(36), nullable=True)
    partner_user_team_id = db.Column(db.String(36), nullable=True)
    helpdesk_user_role_id = db.Column(db.String(36), nullable=True)
    partner_user_role_id = db.Column(db.String(36), nullable=True)
    team_set_id = db.Column(db.String(36), nullable=True)
    created_by = db.Column(db.String(36), nullable=True)
    updated_by = db.Column(db.String(36), nullable=True)
    email_primary = db.Column(db.String(255), nullable=True)
    email_json = db.Column(db.Text, nullable=True) # JSON stored as Text
    phone_primary = db.Column(db.String(255), nullable=True)
    phone_json = db.Column(db.Text, nullable=True)
    customer_type = db.Column(db.String(255), nullable=True)
    account_status = db.Column(db.String(255), nullable=True)
    industry = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.String(255), nullable=True)
    gstin = db.Column(db.String(15), nullable=True)
    pan = db.Column(db.String(10), nullable=True)
    website = db.Column(db.Text, nullable=True)
    address_type = db.Column(db.String(255), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    area = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True) # Important for "Soft Delete" logic
    auto_updated_at = db.Column(db.DateTime, nullable=True)
    auto_updated_by = db.Column(db.String(255), nullable=True)
    migrated_to_tally_branch = db.Column(db.Boolean, default=False, nullable=False)
    latest_comment = db.Column(db.Text, nullable=True)
    assigned_user = db.relationship('User', backref='accounts', lazy=True)

    def __repr__(self):
        return f"<Account {self.name}>"