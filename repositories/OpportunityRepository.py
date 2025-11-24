from models.Opportunity import Opportunity
from config.database import db

class OpportunityRepository:
    @staticmethod
    def add_opportunity(data):
        new_opp = Opportunity(
            name=data.get('name'),
            amount=data.get('amount') or 0,  # Default to 0 if empty
            sales_stage=data.get('sales_stage'),
            probability=data.get('probability') or 0,
            expected_closed_date=data.get('expected_closed_date') or None,
            assigned_user_id=data.get('assigned_user_id'),
            description=data.get('description')
        )
        db.session.add(new_opp)
        db.session.commit()
        return new_opp

    @staticmethod
    def get_all_opportunities():
        # Sort by newest first
        return Opportunity.query.order_by(Opportunity.created_at.desc()).all()

    @staticmethod
    def get_opportunity_by_id(opp_id):
        return Opportunity.query.get(opp_id)

    @staticmethod
    def update_opportunity(opp_id, data):
        opp = Opportunity.query.get(opp_id)
        if opp:
            opp.name = data.get('name', opp.name)
            opp.amount = data.get('amount', opp.amount)
            opp.sales_stage = data.get('sales_stage', opp.sales_stage)
            opp.probability = data.get('probability', opp.probability)
            opp.expected_closed_date = data.get('expected_closed_date') or opp.expected_closed_date
            opp.assigned_user_id = data.get('assigned_user_id', opp.assigned_user_id)
            opp.description = data.get('description', opp.description)
            
            db.session.commit()
        return opp

    @staticmethod
    def delete_opportunity(opp_id):
        opp = Opportunity.query.get(opp_id)
        if opp:
            db.session.delete(opp)
            db.session.commit()
        return opp