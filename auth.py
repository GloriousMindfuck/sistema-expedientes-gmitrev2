from flask import jsonify, request
from app import app, db, Usuario
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(username=data['username']).first()
    
    if usuario and check_password_hash(usuario.password, data['password']):
        access_token = create_access_token(identity=usuario.id)
        return jsonify({
            'access_token': access_token,
            'rol': usuario.rol
        })
    
    return jsonify({'mensaje': 'Credenciales inválidas'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({'mensaje': 'El usuario ya existe'}), 400
    
    nuevo_usuario = Usuario(
        username=data['username'],
        password=generate_password_hash(data['password']),
        rol=data['rol']
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201
