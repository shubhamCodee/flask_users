from flask import Blueprint, render_template, request, redirect, url_for
from services.AccountService import AccountService
from services.UserService import UserService

account_bp = Blueprint('account', __name__)

@account_bp.route('/')
def index():
    accounts = AccountService.get_all_accounts()
    return render_template('accounts/index.html', accounts=accounts)

@account_bp.route('/add', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        AccountService.create_account(request.form)
        return redirect(url_for('account.index'))
    
    # We need users for the "Assigned User" dropdown
    users = UserService.get_all_users()
    return render_template('accounts/add.html', users=users)

@account_bp.route('/update/<string:id>', methods=['GET', 'POST'])
def update_account(id):
    account = AccountService.get_account_by_id(id)
    
    if request.method == 'POST':
        AccountService.update_account(id, request.form)
        return redirect(url_for('account.index'))
    
    # We need users for the dropdown here too
    users = UserService.get_all_users()
    return render_template('accounts/update.html', account=account, users=users)

@account_bp.route('/delete/<string:id>')
def delete_account(id):
    AccountService.delete_account(id)
    return redirect(url_for('account.index'))