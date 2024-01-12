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
    


    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<Post ID: {p.id}. Posted by:{p.posted_by}. Title: {p.title} >"
    

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)