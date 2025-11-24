from models.Lead import Lead
from config.database import db

class LeadRepository:
    @staticmethod
    def add_lead(data):
        new_lead = Lead(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email_primary=data.get('email_primary'),
            phone_primary=data.get('phone_primary'),
            status=data.get('status'),
            lead_source=data.get('lead_source'),
            assigned_user_id=data.get('assigned_user_id'),
            description=data.get('description')
        )
        db.session.add(new_lead)
        db.session.commit()
        return new_lead

    @staticmethod
    def get_all_leads():
        # Sorting by newest first (descending ID) looks better
        return Lead.query.order_by(Lead.created_at.desc()).all()

    @staticmethod
    def get_lead_by_id(lead_id):
        return Lead.query.get(lead_id)

    @staticmethod
    def update_lead(lead_id, data):
        lead = Lead.query.get(lead_id)
        if lead:
            lead.first_name = data.get('first_name', lead.first_name)
            lead.last_name = data.get('last_name', lead.last_name)
            lead.email_primary = data.get('email_primary', lead.email_primary)
            lead.phone_primary = data.get('phone_primary', lead.phone_primary)
            lead.status = data.get('status', lead.status)
            lead.lead_source = data.get('lead_source', lead.lead_source)
            lead.assigned_user_id = data.get('assigned_user_id', lead.assigned_user_id)
            lead.description = data.get('description', lead.description)
            
            db.session.commit()
        return lead

    @staticmethod
    def delete_lead(lead_id):
        lead = Lead.query.get(lead_id)
        if lead:
            db.session.delete(lead)
            db.session.commit()
        return lead