from flask import Blueprint, render_template, request, redirect, url_for
from services.AIService import AIService

ai_bp = Blueprint('ai', __name__)

ai_service = AIService()

@ai_bp.route('/', methods=['GET'])
def index():
    return render_template('ai/index.html')

@ai_bp.route('/train', methods=['POST'])
def train():
    message = ai_service.train_ai()
    
    return render_template('ai/index.html', message=message)

@ai_bp.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('query')

    response_list = ai_service.ask_ai(user_query)
    answer_text = response_list[0]

    return render_template('ai/index.html', answer=answer_text, query=user_query)