import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import db, Usuario

load_dotenv()

def init_database():
    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Crear base de datos si no existe
    cur = conn.cursor()
    try:
        cur.execute("CREATE DATABASE expedientes_db")
        print("Base de datos creada exitosamente")
    except psycopg2.Error as e:
        print(f"La base de datos ya existe o ocurrió un error: {e}")
    finally:
        cur.close()
        conn.close()

def init_tables():
    # Crear tablas
    db.create_all()
    
    # Crear usuario administrador por defecto
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password=generate_password_hash('admin123'),
            rol='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado exitosamente")

if __name__ == '__main__':
    print("Inicializando base de datos...")
    init_database()
    print("Creando tablas y usuario administrador...")
    init_tables()
    print("Inicialización completada")
