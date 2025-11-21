from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from services.UserService import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        
        success = UserService.create_user(username, email)
        
        if success:
            flash("User added successfully!", "success")
        else:
            flash("That email is already taken!", "error")
            
        return redirect(url_for("user.home"))

    users = UserService.get_all_users()
    return render_template("index.html", users=users)

@user_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        
        UserService.update_user(id, username, email)
        
        flash("User updated successfully!", "success")
        return redirect(url_for("user.home"))

    user = UserService.get_user_by_id(id)
    return render_template("update.html", user=user)

@user_bp.route("/delete/<int:id>")
def delete_user(id):
    UserService.delete_user(id)
    flash("User deleted successfully!", "success")
    return redirect(url_for("user.home"))

@user_bp.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query")
        
        ai_service = current_app.ai_service
        
        if query:
            results = ai_service.search_users(query)
            
    return render_template("search.html", results=results, query=query)