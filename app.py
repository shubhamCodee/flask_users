from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "my_super_secret_internship_key"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash("That email is already taken! Try another.", "error")
            return redirect(url_for("home"))
        
        new_user = User(username=username, email=email)

        db.session.add(new_user)
        db.session.commit()
        
        flash("User added successfully!", "success")
        return redirect(url_for("home"))

    all_users = User.query.all()
    return render_template("index.html", users=all_users)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    user_to_update = User.query.get_or_404(id)

    if request.method == "POST":
        user_to_update.username = request.form.get("username")
        user_to_update.email = request.form.get("email")

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("update.html", user=user_to_update)

@app.route("/delete/<int:id>")
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)