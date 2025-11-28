from flask import Blueprint, render_template, request, redirect, url_for
from services.LeadService import LeadService
from services.UserService import UserService

lead_bp = Blueprint('lead', __name__)

@lead_bp.route('/')
def index():
    leads = LeadService.get_all_leads()
    return render_template('leads/index.html', leads=leads)

@lead_bp.route('/view/<string:id>')
def view_lead(id):
    lead = LeadService.get_lead_by_id(id)
    return render_template('leads/view.html', lead=lead)

@lead_bp.route('/add', methods=['GET', 'POST'])
def add_lead():
    if request.method == 'POST':
        LeadService.create_lead(request.form)
        return redirect(url_for('lead.index'))
    
    users = UserService.get_all_users()
    return render_template('leads/add.html', users=users)

@lead_bp.route('/update/<string:id>', methods=['GET', 'POST'])
def update_lead(id):
    lead = LeadService.get_lead_by_id(id)
    
    if request.method == 'POST':
        LeadService.update_lead(id, request.form)
        return redirect(url_for('lead.view_lead', id=id))
    
    users = UserService.get_all_users()
    return render_template('leads/update.html', lead=lead, users=users)

@lead_bp.route('/delete/<string:id>')
def delete_lead(id):
    LeadService.delete_lead(id)
    return redirect(url_for('lead.index'))