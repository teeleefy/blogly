"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()
current_dateTime = datetime.now()

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first = db.Column(db.String(50),
                     nullable=False)
    last = db.Column(db.String(50),
                     nullable=False)
    image = db.Column(db.Text, nullable=False, default='https://icons.veryicon.com/png/o/miscellaneous/two-color-icon-library/user-286.png')
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<My name is {p.first} {p.last}, and my id is {p.id}.>"
    
class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.Text,
                     nullable=False)
    created_at = db.Column(db.DateTime, default=current_dateTime)
    user_id = db.Column(db.Integer,
                          db.ForeignKey("users.id"),
                          nullable=False)
    tags = db.relationship('Tag',
                               secondary='post_tags',
                               backref='posts')
    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<Post ID: {p.id}. Posted by:{p.user_id}. Title: {p.title}.>"
    
class PostTag(db.Model):
    """Post Tags Join Table."""

    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer, 
                          db.ForeignKey("posts.id"), primary_key=True,
                          nullable=False)
    tag_id = db.Column(db.Integer, 
                          db.ForeignKey("tags.id"), primary_key=True,
                          nullable=False)
    
    def __repr__(self):
        """Show info about post_tag."""
        p = self
        return f"<Post ID: {p.post_id}. Tag ID:{p.tag_id}.>"
    
class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False, unique=True)
    
    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<Tag ID: {p.id}. Tag name:{p.name}. >"


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)