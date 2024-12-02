import pytest
from app import app as flask_app, db
from models import Usuario
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with flask_app.app_context():
        db.create_all()
        
        # Crear usuario de prueba
        admin = Usuario(
            username='admin_test',
            password=generate_password_hash('password'),
            rol='admin'
        )
        db.session.add(admin)
        db.session.commit()
        
        yield flask_app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    response = client.post('/api/auth/login', json={
        'username': 'admin_test',
        'password': 'password'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
