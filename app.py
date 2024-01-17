"""Blogly application."""
# flask imports
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

# sql imports
from models import db, connect_db, User, Post, PostTag, Tag

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

# Use the three lines below to drop the tables in the database and recreate them
# with app.app_context():
#     db.drop_all()
#     db.create_all()
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
    posts = Post.query.filter_by(user_id = user_id).all()
    return render_template("profile.html", user=user, posts = posts)

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
























#-------------------POSTS SECTION----------------------------------------------------------
#Make a route for adding posts. It will be a direct render_template
@app.route("/users/<int:user_id>/add_post")
def add_post(user_id):
    """Direct user to add post page."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("/posts/add_post.html", user=user, tags = tags)

#Make a route for saving posts.  It will handle the form data, and update database. Then it will redirect you to your post url.
@app.route("/users/<int:users_id>/save_post", methods=["POST"])
def save_post(users_id):
    """Add post and redirect to post's page."""
    user = User.query.get_or_404(users_id)
    title = request.form['title']
    content = request.form['content']
    post_tags = [int(num) for num in request.form.getlist('tag')]
    tags = Tag.query.filter(Tag.id.in_(post_tags)).all()
    post = Post(title=title, content=content, user_id = users_id, tags = tags)
    db.session.add(post)   
    db.session.commit()
    # return render_template('/tags/experiment.html', tags = post_tags)
    return redirect(f"/users/{user.id}/posts/{post.id}")

# #This will be your post page.  It will also have links that lead to the edit pages and the delete option.
# /users/{user.id}/posts/{post.id}
@app.route("/users/<int:user_id>/posts/<int:post_id>")
def see_post(user_id, post_id):
    """Direct user to add post page."""
    user = User.query.get_or_404(user_id)
    post = Post.query.filter_by(id = post_id).one()
    
    return render_template("/posts/post.html", user=user, post=post)


# #This is a link to the edit page.  It will render template of the edit_post.html
# /users/{{user.id}}/posts/{{post.id}}/edit
@app.route("/users/<int:user_id>/posts/<int:post_id>/edit")
def edit_post(user_id, post_id):
    """Edit info on a single user."""
    user = User.query.get_or_404(user_id)
    post = Post.query.filter_by(id = post_id).one()
    tags = Tag.query.all()
    return render_template("/posts/edit_post.html", user=user, post=post, tags=tags)


#This is a redirect link.  It will handle the form data and update the post in the database. It will then redirect you to the newly updated post's page.
@app.route("/users/<int:user_id>/posts/<int:post_id>/update", methods=["POST"])
def update_post(user_id, post_id):
    """Update post when edited."""
    user = User.query.get_or_404(user_id)
    post = Post.query.filter_by(id = post_id).one()
    #get form content
    title = request.form['title']
    content = request.form['content']
    post_tags = [int(num) for num in request.form.getlist('tag')]
    tags = Tag.query.filter(Tag.id.in_(post_tags)).all()
    #update post in database
    post.title = title
    post.content = content
    post.tags = tags
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user.id}/posts/{post.id}")


# #This is a redirect link.  It will remove the post from the database.  Then it will redirect you to the user's profile page. 
# /users/{{user.id}}/posts/{{post.id}}/delete
@app.route("/users/<int:user_id>/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(user_id, post_id):
    """Delete post and redirect to updated User profile page."""
    user = User.query.get_or_404(user_id)
    post = Post.query.filter_by(id = post_id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user.id}")




#---------------------------------Many-to-Many-----------------------------------

### ****Add Routes****


# **GET */tags :*** Lists all tags, with links to the tag detail page.
@app.route("/tags")
def list_tags():
    """List tags."""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("/tags/list_tags.html", tags=tags)


# **GET */tags/[tag-id] :*** Show detail about a tag. Have links to edit form and to delete.
@app.route("/tags/<int:tag_id>")
def see_tag(tag_id):
    """Direct user to a tag's page."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tags/show_tag.html", tag=tag)

# **GET */tags/new :*** Shows a form to add a new tag.
# **POST */tags/new :*** Process add form, adds tag, and redirect to tag list.
@app.route('/tags/new', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        tag_name = request.form['name']
        tag = Tag(name = tag_name)
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags")
    else:
        return render_template("/tags/add_tag.html")






# **GET */tags/[tag-id]/edit :*** Show edit form for a tag.
# **POST */tags/[tag-id]/edit :*** Process edit form, edit tag, and redirects to the tags list.
@app.route("/tags/<int:tag_id>/edit", methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit info on a single tag."""
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        tag_name = request.form['name']
        tag.name = tag_name
        db.session.add(tag)
        db.session.commit()
        return redirect(f"/tags/{tag_id}")
    else:
        return render_template("/tags/edit_tag.html", tag=tag)


# **POST */tags/[tag-id]/delete :*** Delete a tag.
@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag and redirect to updated list of tags."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")

