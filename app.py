from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///expedientes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'admin' o 'consultor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    color = db.Column(db.String(20))
    color_bibliorato = db.Column(db.String(20))
    estado = db.Column(db.String(20))  # Pagado, Abierto, Cerrado, Pendiente, Faltan Firmas
    monto = db.Column(db.Float)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_pago = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    accion = db.Column(db.String(50))
    detalles = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# Crear las tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Permitir conexiones desde cualquier IP en la red local
    app.run(host='0.0.0.0', port=5000, debug=True)
