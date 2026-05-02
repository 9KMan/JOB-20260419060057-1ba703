import unittest
from app import create_app, db
from app.models import User, Artist, Venue, Booking

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with self.app.app_context():
            user = User(email='test@example.com', name='Test User')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            retrieved = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(retrieved)
            self.assertTrue(retrieved.check_password('password123'))

    def test_artist_creation(self):
        with self.app.app_context():
            user = User(email='artist@example.com', name='Artist User')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            artist = Artist(user_id=user.id, name='Test Artist', genre='Jazz', hourly_rate=50.0)
            db.session.add(artist)
            db.session.commit()
            retrieved = Artist.query.first()
            self.assertEqual(retrieved.name, 'Test Artist')

    def test_venue_creation(self):
        with self.app.app_context():
            user = User(email='venue@example.com', name='Venue Owner')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            venue = Venue(user_id=user.id, name='Test Venue', address='123 Test St', capacity=200)
            db.session.add(venue)
            db.session.commit()
            retrieved = Venue.query.first()
            self.assertEqual(retrieved.name, 'Test Venue')
            self.assertEqual(retrieved.capacity, 200)

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post('/api/auth/register',
            json={'email': 'new@example.com', 'password': 'password123', 'name': 'New User'})
        self.assertEqual(response.status_code, 201)

    def test_get_artists(self):
        response = self.client.get('/api/artists')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
