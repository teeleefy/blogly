from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class UsersTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            User.query.delete()

            user = User(first="Flower", last="Power", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6njAYMm91UmTViYt7rf7U9BpKxYN2wV0FSHQkyQOHx1hoj_KXr7a5roTNDdYiQGJDcuI&usqp=CAU")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Flower', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Flower Power</h1>', html)

    def test_add_user(self):
        
            with app.test_client() as client:
                with app.app_context():
                    d = {"first": "Mickey", "last": "Mouse", "image" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbuSxOVmvZ5uCNl5Ep5zLvwMGpalfsCrPPS9vYqCy95R-AuelWYApJ9_4Q4poKQ97jOXQ&usqp=CAU"}
                    resp = client.post("/save", data=d, follow_redirects=True)
                    html = resp.get_data(as_text=True)
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn("<h1>Mickey Mouse</h1>", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<h1>Flower Power</h1>", html)
            
            
