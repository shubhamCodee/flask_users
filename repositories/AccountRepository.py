from models.Account import Account
from config.database import db

class AccountRepository:
    
    @staticmethod
    def add_account(data):
        new_account = Account(
            name=data.get('name'),
            description=data.get('description'),
            assigned_user_id=data.get('assigned_user_id') or None, # Handle empty string as None
            email_primary=data.get('email_primary'),
            email_json=data.get('email_json'),
            phone_primary=data.get('phone_primary'),
            phone_json=data.get('phone_json'),
            website=data.get('website'),
            industry=data.get('industry'),
            rating=data.get('rating'),
            customer_type=data.get('customer_type'),
            account_status=data.get('account_status'),
            gstin=data.get('gstin'),
            pan=data.get('pan'),
            migrated_to_tally_branch=True if data.get('migrated_to_tally_branch') == 'true' else False,
            address_type=data.get('address_type'),
            street=data.get('street'),
            area=data.get('area'),
            city=data.get('city'),
            state=data.get('state'),
            country=data.get('country'),
            postal_code=data.get('postal_code'),
            team_id=data.get('team_id'),
            helpdesk_user_team_id=data.get('helpdesk_user_team_id'),
            partner_user_team_id=data.get('partner_user_team_id'),
            helpdesk_user_role_id=data.get('helpdesk_user_role_id'),
            partner_user_role_id=data.get('partner_user_role_id'),
            team_set_id=data.get('team_set_id'),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by'),
            auto_updated_by=data.get('auto_updated_by'),
            latest_comment=data.get('latest_comment')
        )
        
        db.session.add(new_account)
        db.session.commit()
        return new_account

    @staticmethod
    def get_all_accounts():
        return Account.query.order_by(Account.created_at.desc()).all()

    @staticmethod
    def get_account_by_id(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def update_account(account_id, data):
        account = Account.query.get(account_id)
        if account:
            account.name = data.get('name', account.name)
            account.description = data.get('description', account.description)
            account.assigned_user_id = data.get('assigned_user_id') or None
            account.email_primary = data.get('email_primary', account.email_primary)
            account.email_json = data.get('email_json', account.email_json)
            account.phone_primary = data.get('phone_primary', account.phone_primary)
            account.phone_json = data.get('phone_json', account.phone_json)
            account.website = data.get('website', account.website)
            account.industry = data.get('industry', account.industry)
            account.rating = data.get('rating', account.rating)
            account.customer_type = data.get('customer_type', account.customer_type)
            account.account_status = data.get('account_status', account.account_status)
            account.gstin = data.get('gstin', account.gstin)
            account.pan = data.get('pan', account.pan)
            if 'migrated_to_tally_branch' in data:
                 account.migrated_to_tally_branch = True if data.get('migrated_to_tally_branch') == 'true' else False
            account.address_type = data.get('address_type', account.address_type)
            account.street = data.get('street', account.street)
            account.area = data.get('area', account.area)
            account.city = data.get('city', account.city)
            account.state = data.get('state', account.state)
            account.country = data.get('country', account.country)
            account.postal_code = data.get('postal_code', account.postal_code)
            account.team_id = data.get('team_id', account.team_id)
            account.helpdesk_user_team_id = data.get('helpdesk_user_team_id', account.helpdesk_user_team_id)
            account.partner_user_team_id = data.get('partner_user_team_id', account.partner_user_team_id)
            account.helpdesk_user_role_id = data.get('helpdesk_user_role_id', account.helpdesk_user_role_id)
            account.partner_user_role_id = data.get('partner_user_role_id', account.partner_user_role_id)
            account.team_set_id = data.get('team_set_id', account.team_set_id)
            account.updated_by = data.get('updated_by', account.updated_by)
            account.auto_updated_by = data.get('auto_updated_by', account.auto_updated_by)
            account.latest_comment = data.get('latest_comment', account.latest_comment)
            
            db.session.commit()
        return account

    @staticmethod
    def delete_account(account_id):
        account = Account.query.get(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()
        return account