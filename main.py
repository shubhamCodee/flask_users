import os
from flask import Flask, render_template
from dotenv import load_dotenv
load_dotenv()

from config.database import db
from controllers.UserController import user_bp
from controllers.AccountController import account_bp
from controllers.LeadController import lead_bp
from controllers.OpportunityController import opportunity_bp
from controllers.AIController import ai_bp
from controllers.WebhookController import webhook_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/users')

    app.register_blueprint(account_bp, url_prefix='/accounts')

    app.register_blueprint(lead_bp, url_prefix='/leads')

    app.register_blueprint(opportunity_bp, url_prefix='/opportunities')

    app.register_blueprint(ai_bp, url_prefix='/ai')

    app.register_blueprint(webhook_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    
    app.run(debug=True)