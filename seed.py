"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
whiskey = User(first='Whiskey', last="Todd", image='https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQmEJdaok07spk0FGsCi-XmAOWBrvfeDXmpZnV6GBjZxpNqsmI4mzVvXa9Prpa0NbBbu2RaXFS6HHNMGIatJhL1GFplSqJQS3lAWkuM1k8oIN6smePSpKFKpkk')
bowser = User(first='Bowser', last="Todd", image='')
spike = User(first='Spike', last="Todd")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
# Commit--otherwise, this never gets saved!
db.session.commit()
