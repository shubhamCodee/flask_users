import os
from flask import Flask
from dotenv import load_dotenv
from config.database import db
from controllers.UserController import user_bp
from services.AIService import AIService
from services.UserService import UserService

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/users')

    with app.app_context():
        db.create_all()

        ai_service = AIService()
        
        all_users = UserService.get_all_users()
        
        ai_service.train_with_users(all_users)
        
        app.ai_service = ai_service

    return app

if __name__ == "__main__":
    app = create_app()
    
    app.run(debug=True)