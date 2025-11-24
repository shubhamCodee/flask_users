from repositories.AccountRepository import AccountRepository

class AccountService:
    @staticmethod
    def create_account(data):
        # In the future, we can add AI Training logic here
        return AccountRepository.add_account(data)

    @staticmethod
    def get_all_accounts():
        return AccountRepository.get_all_accounts()

    @staticmethod
    def get_account_by_id(account_id):
        return AccountRepository.get_account_by_id(account_id)

    @staticmethod
    def update_account(account_id, data):
        return AccountRepository.update_account(account_id, data)

    @staticmethod
    def delete_account(account_id):
        return AccountRepository.delete_account(account_id)