from flask import Blueprint, request, jsonify
from config.database import db
from models.Lead import Lead
from datetime import datetime

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhooks/n8n/create-lead', methods=['POST'])
def create_lead_from_n8n():
    data = request.json
    
    new_lead = Lead(
        first_name=data.get('first_name', 'Unknown'),  # Mapping to first_name so __repr__ works
        email_primary=data.get('email', 'no_email@provided.com'),
        description=data.get('description', ''), 
        latest_comment=data.get('subject', 'No Subject'),
        lead_source="Email Integration (n8n)",
        status="New",
        created_by="n8n-bot",
        created_at=datetime.utcnow()
    )

    db.session.add(new_lead)
    db.session.commit()

    return jsonify({"message": "Lead Created", "id": new_lead.id}), 201