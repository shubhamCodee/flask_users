from models.Account import Account
from config.database import db

class AccountRepository:
    @staticmethod
    def add_account(data):
        # We use .get() to avoid errors if the field is missing in the form
        new_account = Account(
            name=data.get('name'),
            email_primary=data.get('email_primary'),
            phone_primary=data.get('phone_primary'),
            industry=data.get('industry'),
            assigned_user_id=data.get('assigned_user_id') # Linking to a User
        )
        db.session.add(new_account)
        db.session.commit()
        return new_account

    @staticmethod
    def get_all_accounts():
        return Account.query.all()

    @staticmethod
    def get_account_by_id(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def update_account(account_id, data):
        account = Account.query.get(account_id)
        if account:
            account.name = data.get('name', account.name)
            account.email_primary = data.get('email_primary', account.email_primary)
            account.phone_primary = data.get('phone_primary', account.phone_primary)
            account.industry = data.get('industry', account.industry)
            account.assigned_user_id = data.get('assigned_user_id', account.assigned_user_id)
            
            db.session.commit()
        return account

    @staticmethod
    def delete_account(account_id):
        account = Account.query.get(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()
        return account