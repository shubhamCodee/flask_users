from repositories.UserRepository import UserRepository

class UserService:
    
    @staticmethod
    def create_user(username, email):
        existing_user = UserRepository.get_user_by_email(email)
        
        if existing_user:
            return False 
            
        UserRepository.create_user(username, email)
        return True 

    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_user(user_id, username, email):
        user = UserRepository.get_user_by_id(user_id)
        
        UserRepository.update_user(user, username, email)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        
        UserRepository.delete_user(user)