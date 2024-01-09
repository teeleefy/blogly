"""Blogly application."""
# flask imports
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

# sql imports
from models import db, connect_db, User

# app configuration
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "MYSECRET"

# setup flask debug toolbar

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# connect to database
connect_db(app)
# db.create_all()

#--------------------------------------------------------------------------------------
# **Make routes for the following:**

# **GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
@app.route("/")
def update_users():
    """Redirect to users."""
    return redirect("/users")


# **GET */users :*** Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
@app.route("/users")
def list_users():
    """List users and show button linking to add form."""
    users = User.query.order_by(User.last, User.first).all()
    return render_template("users.html", users=users)


# **GET */users/new :*** Show an add form for users
@app.route("/users/new")
def add_form():
    """Show add form."""
    return render_template("form.html")

# **POST */users/new :*** Process the add form, adding a new user and going back to ***/users***

@app.route("/save", methods=["POST"])
def add_user():
    """Add user and redirect to user profile."""
    first = request.form['first']
    last = request.form['last']
    image = request.form['image']
    image = image if image else None
    user = User(first=first, last=last, image=image)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

# **GET */users/[user-id] :***Show information about the given user. Have a button to get to their edit page, and to delete the user.

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)

# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


# **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.

@app.route("/users/<int:user_id>/update", methods=["POST"])
def update_user(user_id):
    """Update info on a single user."""
    user = User.query.get_or_404(user_id)
    first = request.form['first']
    last = request.form['last']
    image = request.form['image']
    image = image if image else "https://icons.veryicon.com/png/o/miscellaneous/two-color-icon-library/user-286.png"
    user.first = first
    user.last = last
    user.image = image
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user.id}")

# **POST */users/[user-id]/delete :*** Delete the user.
@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to updated list of users."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")