import socket
import netifaces
import os

def get_local_ip():
    # Obtener la IP local del servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def setup_network_config():
    local_ip = get_local_ip()
    print(f"IP local detectada: {local_ip}")
    
    # Actualizar .env del backend
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('CORS_ORIGINS='):
                f.write(f'CORS_ORIGINS=http://{local_ip}:3000\n')
            else:
                f.write(line)
    
    # Actualizar .env del frontend
    frontend_env = f"""REACT_APP_API_URL=http://{local_ip}:5000
REACT_APP_ENV=production"""
    
    with open('frontend/.env', 'w') as f:
        f.write(frontend_env)
    
    print("""
Configuración de red completada:
1. Backend: Ejecutar 'python app.py'
2. Frontend: Ejecutar 'cd frontend && npm start'

Para acceder desde otras PCs en la red:
- Backend: http://{local_ip}:5000
- Frontend: http://{local_ip}:3000

Asegúrate de que:
1. El firewall permita conexiones a los puertos 5000 y 3000
2. Todas las PCs estén en la misma red
3. El servidor PostgreSQL permita conexiones remotas
""".format(local_ip=local_ip))

if __name__ == '__main__':
    setup_network_config()
