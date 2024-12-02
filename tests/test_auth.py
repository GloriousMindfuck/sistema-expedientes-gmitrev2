import pytest
from app import db
from models import Usuario
from werkzeug.security import generate_password_hash

def test_login_exitoso(client):
    response = client.post('/api/auth/login', json={
        'username': 'admin_test',
        'password': 'password'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'rol' in response.json
    assert response.json['rol'] == 'admin'

def test_login_fallido(client):
    response = client.post('/api/auth/login', json={
        'username': 'admin_test',
        'password': 'wrong_password'
    })
    
    assert response.status_code == 401
    assert 'mensaje' in response.json
    assert response.json['mensaje'] == 'Credenciales inválidas'

def test_registro_usuario(client, auth_headers):
    response = client.post('/api/auth/register', json={
        'username': 'nuevo_usuario',
        'password': 'password123',
        'rol': 'consultor'
    }, headers=auth_headers)
    
    assert response.status_code == 201
    
    usuario = Usuario.query.filter_by(username='nuevo_usuario').first()
    assert usuario is not None
    assert usuario.rol == 'consultor'

def test_acceso_protegido(client):
    # Intentar acceder sin token
    response = client.get('/api/expedientes')
    assert response.status_code == 401
    
    # Intentar acceder con token inválido
    response = client.get('/api/expedientes', headers={
        'Authorization': 'Bearer invalid_token'
    })
    assert response.status_code == 422
