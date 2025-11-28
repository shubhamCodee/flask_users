from flask import Blueprint, render_template, request, redirect, url_for
from services.OpportunityService import OpportunityService
from services.UserService import UserService

opportunity_bp = Blueprint('opportunity', __name__)

@opportunity_bp.route('/')
def index():
    opportunities = OpportunityService.get_all_opportunities()
    return render_template('opportunities/index.html', opportunities=opportunities)

@opportunity_bp.route('/view/<string:id>')
def view_opportunity(id):
    opportunity = OpportunityService.get_opportunity_by_id(id)
    return render_template('opportunities/view.html', opportunity=opportunity)

@opportunity_bp.route('/add', methods=['GET', 'POST'])
def add_opportunity():
    if request.method == 'POST':
        OpportunityService.create_opportunity(request.form)
        return redirect(url_for('opportunity.index'))
    
    users = UserService.get_all_users()
    return render_template('opportunities/add.html', users=users)

@opportunity_bp.route('/update/<string:id>', methods=['GET', 'POST'])
def update_opportunity(id):
    opportunity = OpportunityService.get_opportunity_by_id(id)
    
    if request.method == 'POST':
        OpportunityService.update_opportunity(id, request.form)
        return redirect(url_for('opportunity.view_opportunity', id=id))
    
    users = UserService.get_all_users()
    return render_template('opportunities/update.html', opportunity=opportunity, users=users)

@opportunity_bp.route('/delete/<string:id>')
def delete_opportunity(id):
    OpportunityService.delete_opportunity(id)
    return redirect(url_for('opportunity.index'))