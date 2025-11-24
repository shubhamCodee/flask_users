from config.database import db
from datetime import datetime
import uuid

class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    assigned_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    team_id = db.Column(db.String(36), nullable=True)
    team_set_id = db.Column(db.String(36), nullable=True)
    created_by = db.Column(db.String(36), nullable=True)
    updated_by = db.Column(db.String(36), nullable=True)
    opportunity_number = db.Column(db.Integer, autoincrement=True, nullable=False)
    sales_stage = db.Column(db.String(255), nullable=True)
    probability = db.Column(db.Numeric(16, 2), nullable=True)
    opportunity_type = db.Column(db.String(255), nullable=True)
    expected_closed_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Numeric(16, 2), nullable=True)
    gross_profit = db.Column(db.Numeric(16, 2), nullable=True)
    quantity = db.Column(db.Numeric(16, 2), nullable=True)
    product_sub_category = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(255), nullable=True)
    customer_type = db.Column(db.String(255), nullable=True)
    lead_source = db.Column(db.String(255), nullable=True)
    lost_reason = db.Column(db.String(255), nullable=True)
    closed_date = db.Column(db.Date, nullable=True)
    last_contract_id = db.Column(db.String(36), nullable=True)
    next_followup_date = db.Column(db.DateTime, nullable=True)
    next_followup_type = db.Column(db.String(255), nullable=True)
    how_old_days = db.Column(db.Integer, nullable=True)
    untouched_since_days = db.Column(db.Integer, nullable=True)
    contract_automation = db.Column(db.Boolean, default=False)
    lead_created_date = db.Column(db.DateTime, nullable=True)
    lead_created_tat_hours = db.Column(db.Integer, nullable=True)
    lead_created_tat = db.Column(db.DateTime, nullable=True)
    current_opportunity = db.Column(db.Boolean, default=False)
    contract_created = db.Column(db.Boolean, default=False)
    how_old = db.Column(db.String(255), nullable=True)
    untouched_since = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    auto_updated_at = db.Column(db.DateTime, nullable=True)
    auto_updated_by = db.Column(db.String(255), nullable=True)
    auto_product_created = db.Column(db.Boolean, default=False)
    latest_comment = db.Column(db.Text, nullable=True)
    assigned_user = db.relationship('User', backref='opportunities', lazy=True)
    
    def __repr__(self):
        return f"<Opportunity {self.name}>"