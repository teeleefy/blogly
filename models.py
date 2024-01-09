"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<My name is {p.first} {p.last}, and my id is {p.id}.>"
    

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)