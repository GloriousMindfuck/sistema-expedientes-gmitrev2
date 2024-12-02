from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # Verificar si el usuario ya existe
        admin = Usuario.query.filter_by(username='admin').first()
        if admin:
            print("El usuario admin ya existe. Actualizando contraseña...")
            admin.password = generate_password_hash('admin123')
        else:
            print("Creando usuario administrador...")
            admin = Usuario(
                username='admin',
                password=generate_password_hash('admin123'),
                rol='admin'
            )
            db.session.add(admin)
        
        db.session.commit()
        print("Usuario administrador configurado exitosamente")

if __name__ == '__main__':
    create_admin()
