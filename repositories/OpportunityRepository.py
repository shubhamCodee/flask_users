from models.Opportunity import Opportunity
from config.database import db

class OpportunityRepository:
    
    @staticmethod
    def add_opportunity(data):
        new_opp = Opportunity(
            name=data.get('name'),
            description=data.get('description'),
            assigned_user_id=data.get('assigned_user_id') or None,
            amount=data.get('amount') or 0,
            gross_profit=data.get('gross_profit') or 0,
            quantity=data.get('quantity') or 0,
            probability=data.get('probability') or 0,
            sales_stage=data.get('sales_stage'),
            opportunity_type=data.get('opportunity_type'),
            lead_source=data.get('lead_source'),
            lost_reason=data.get('lost_reason'),
            priority=data.get('priority'),
            customer_type=data.get('customer_type'),
            product_sub_category=data.get('product_sub_category'),
            expected_closed_date=data.get('expected_closed_date') or None,
            closed_date=data.get('closed_date') or None,
            next_followup_date=data.get('next_followup_date') or None,
            next_followup_type=data.get('next_followup_type'),
            contract_automation=True if data.get('contract_automation') == 'true' else False,
            current_opportunity=True if data.get('current_opportunity') == 'true' else False,
            contract_created=True if data.get('contract_created') == 'true' else False,
            auto_product_created=True if data.get('auto_product_created') == 'true' else False,
            team_id=data.get('team_id'),
            team_set_id=data.get('team_set_id'),
            last_contract_id=data.get('last_contract_id'),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by'),
            auto_updated_by=data.get('auto_updated_by'),
            how_old_days=data.get('how_old_days') or None,
            untouched_since_days=data.get('untouched_since_days') or None,
            how_old=data.get('how_old'),
            untouched_since=data.get('untouched_since'),
            lead_created_date=data.get('lead_created_date') or None,
            lead_created_tat_hours=data.get('lead_created_tat_hours') or None,
            lead_created_tat=data.get('lead_created_tat') or None,
            latest_comment=data.get('latest_comment')
        )
        
        db.session.add(new_opp)
        db.session.commit()
        return new_opp

    @staticmethod
    def get_all_opportunities():
        return Opportunity.query.order_by(Opportunity.created_at.desc()).all()

    @staticmethod
    def get_opportunity_by_id(opp_id):
        return Opportunity.query.get(opp_id)

    @staticmethod
    def update_opportunity(opp_id, data):
        opp = Opportunity.query.get(opp_id)
        if opp:
            opp.name = data.get('name', opp.name)
            opp.description = data.get('description', opp.description)
            opp.assigned_user_id = data.get('assigned_user_id') or None
            opp.amount = data.get('amount', opp.amount)
            opp.gross_profit = data.get('gross_profit', opp.gross_profit)
            opp.quantity = data.get('quantity', opp.quantity)
            opp.probability = data.get('probability', opp.probability)
            opp.sales_stage = data.get('sales_stage', opp.sales_stage)
            opp.opportunity_type = data.get('opportunity_type', opp.opportunity_type)
            opp.lead_source = data.get('lead_source', opp.lead_source)
            opp.lost_reason = data.get('lost_reason', opp.lost_reason)
            opp.priority = data.get('priority', opp.priority)
            opp.customer_type = data.get('customer_type', opp.customer_type)
            opp.product_sub_category = data.get('product_sub_category', opp.product_sub_category)
            opp.expected_closed_date = data.get('expected_closed_date') or None
            opp.closed_date = data.get('closed_date') or None
            opp.next_followup_date = data.get('next_followup_date') or None
            opp.next_followup_type = data.get('next_followup_type', opp.next_followup_type)

            if 'contract_automation' in data:
                opp.contract_automation = True if data.get('contract_automation') == 'true' else False
            else:
                opp.contract_automation = False

            if 'current_opportunity' in data:
                opp.current_opportunity = True if data.get('current_opportunity') == 'true' else False
            else:
                opp.current_opportunity = False
                
            if 'contract_created' in data:
                opp.contract_created = True if data.get('contract_created') == 'true' else False
            else:
                opp.contract_created = False
                
            if 'auto_product_created' in data:
                opp.auto_product_created = True if data.get('auto_product_created') == 'true' else False
            else:
                opp.auto_product_created = False
            
            opp.team_id = data.get('team_id', opp.team_id)
            opp.team_set_id = data.get('team_set_id', opp.team_set_id)
            opp.last_contract_id = data.get('last_contract_id', opp.last_contract_id)
            opp.updated_by = data.get('updated_by', opp.updated_by)
            opp.auto_updated_by = data.get('auto_updated_by', opp.auto_updated_by)
            opp.how_old_days = data.get('how_old_days') or None
            opp.untouched_since_days = data.get('untouched_since_days') or None
            opp.how_old = data.get('how_old', opp.how_old)
            opp.untouched_since = data.get('untouched_since', opp.untouched_since)
            opp.lead_created_date = data.get('lead_created_date') or None
            opp.lead_created_tat_hours = data.get('lead_created_tat_hours') or None
            opp.lead_created_tat = data.get('lead_created_tat') or None
            opp.latest_comment = data.get('latest_comment', opp.latest_comment)

            db.session.commit()
        return opp

    @staticmethod
    def delete_opportunity(opp_id):
        opp = Opportunity.query.get(opp_id)
        if opp:
            db.session.delete(opp)
            db.session.commit()
        return opp