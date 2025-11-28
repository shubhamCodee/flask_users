from models.Lead import Lead
from config.database import db

class LeadRepository:
    
    @staticmethod
    def add_lead(data):
        new_lead = Lead(
            salutation=data.get('salutation'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            email_primary=data.get('email_primary'),
            email_json=data.get('email_json'),
            phone_primary=data.get('phone_primary'),
            phone_json=data.get('phone_json'),
            website=data.get('website'),
            designation=data.get('designation'),
            department=data.get('department'),
            hierarchy=data.get('hierarchy'),
            customer_type=data.get('customer_type'),
            industry=data.get('industry'),
            product_sub_category=data.get('product_sub_category'),
            lead_source=data.get('lead_source'),
            other_source=data.get('other_source'),
            status=data.get('status'),
            lost_reason=data.get('lost_reason'),
            converted=True if data.get('converted') == 'true' else False,
            closed_date=data.get('closed_date') or None,
            next_followup_date=data.get('next_followup_date') or None,
            next_followup_type=data.get('next_followup_type'),
            address_type=data.get('address_type'),
            street=data.get('street'),
            area=data.get('area'),
            city=data.get('city'),
            state=data.get('state'),
            country=data.get('country'),
            postal_code=data.get('postal_code'),
            geofence_radius=data.get('geofence_radius'),
            geofence_latitude=data.get('geofence_latitude'),
            geofence_longitude=data.get('geofence_longitude'),
            how_old_days=data.get('how_old_days') or None,
            untouched_since_days=data.get('untouched_since_days') or None,
            how_old=data.get('how_old'),
            untouched_since=data.get('untouched_since'),
            assigned_user_id=data.get('assigned_user_id') or None,
            account_id_name=data.get('account_id_name'),
            team_id=data.get('team_id'),
            team_set_id=data.get('team_set_id'),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by'),
            auto_updated_by=data.get('auto_updated_by'),
            latest_comment=data.get('latest_comment')
        )
        
        db.session.add(new_lead)
        db.session.commit()
        return new_lead

    @staticmethod
    def get_all_leads():
        return Lead.query.order_by(Lead.created_at.desc()).all()

    @staticmethod
    def get_lead_by_id(lead_id):
        return Lead.query.get(lead_id)

    @staticmethod
    def update_lead(lead_id, data):
        lead = Lead.query.get(lead_id)
        if lead:
            lead.salutation = data.get('salutation', lead.salutation)
            lead.first_name = data.get('first_name', lead.first_name)
            lead.last_name = data.get('last_name', lead.last_name)
            lead.name = data.get('name', lead.name)
            lead.email_primary = data.get('email_primary', lead.email_primary)
            lead.email_json = data.get('email_json', lead.email_json)
            lead.phone_primary = data.get('phone_primary', lead.phone_primary)
            lead.phone_json = data.get('phone_json', lead.phone_json)
            lead.website = data.get('website', lead.website)
            lead.designation = data.get('designation', lead.designation)
            lead.department = data.get('department', lead.department)
            lead.hierarchy = data.get('hierarchy', lead.hierarchy)
            lead.customer_type = data.get('customer_type', lead.customer_type)
            lead.industry = data.get('industry', lead.industry)
            lead.product_sub_category = data.get('product_sub_category', lead.product_sub_category)
            lead.lead_source = data.get('lead_source', lead.lead_source)
            lead.other_source = data.get('other_source', lead.other_source)
            lead.status = data.get('status', lead.status)
            lead.lost_reason = data.get('lost_reason', lead.lost_reason)
            if 'converted' in data:
                lead.converted = True if data.get('converted') == 'true' else False
            else:
                lead.converted = False
            lead.closed_date = data.get('closed_date') or None
            lead.next_followup_date = data.get('next_followup_date') or None
            lead.next_followup_type = data.get('next_followup_type', lead.next_followup_type)
            lead.address_type = data.get('address_type', lead.address_type)
            lead.street = data.get('street', lead.street)
            lead.area = data.get('area', lead.area)
            lead.city = data.get('city', lead.city)
            lead.state = data.get('state', lead.state)
            lead.country = data.get('country', lead.country)
            lead.postal_code = data.get('postal_code', lead.postal_code)
            lead.geofence_radius = data.get('geofence_radius', lead.geofence_radius)
            lead.geofence_latitude = data.get('geofence_latitude', lead.geofence_latitude)
            lead.geofence_longitude = data.get('geofence_longitude', lead.geofence_longitude)
            lead.how_old_days = data.get('how_old_days') or None
            lead.untouched_since_days = data.get('untouched_since_days') or None
            lead.how_old = data.get('how_old', lead.how_old)
            lead.untouched_since = data.get('untouched_since', lead.untouched_since)
            lead.assigned_user_id = data.get('assigned_user_id') or None
            lead.account_id_name = data.get('account_id_name', lead.account_id_name)
            lead.team_id = data.get('team_id', lead.team_id)
            lead.team_set_id = data.get('team_set_id', lead.team_set_id)
            lead.updated_by = data.get('updated_by', lead.updated_by)
            lead.auto_updated_by = data.get('auto_updated_by', lead.auto_updated_by)
            lead.latest_comment = data.get('latest_comment', lead.latest_comment)

            db.session.commit()
        return lead

    @staticmethod
    def delete_lead(lead_id):
        lead = Lead.query.get(lead_id)
        if lead:
            db.session.delete(lead)
            db.session.commit()
        return lead