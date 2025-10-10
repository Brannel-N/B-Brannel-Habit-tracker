from app import app
from models import db, User

TEST_USERNAME = 'test_user_for_cli'

with app.app_context():
    # remove existing test user if present
    existing = User.query.filter_by(username=TEST_USERNAME).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    client = app.test_client()
    resp = client.post('/register', data={'username': TEST_USERNAME, 'password': 'password123'}, follow_redirects=True)
    print('POST /register status:', resp.status_code)
    text = resp.get_data(as_text=True)
    print('Response length:', len(text))

    # verify user exists in DB
    u = User.query.filter_by(username=TEST_USERNAME).first()
    print('User created:', bool(u), 'id:', getattr(u, 'id', None))
