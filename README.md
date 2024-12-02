# Sistema de Gestión de Expedientes - Municipalidad de Guardia Mitre

Sistema integral para la gestión de expedientes municipales con características avanzadas de búsqueda, exportación y respaldo.

## Características Principales

- Gestión completa de expedientes municipales
- Sistema de colores para expedientes y biblioratos
- Búsqueda avanzada con múltiples filtros
- Exportación a Excel
- Copias de seguridad en JSON/CSV
- Sistema de roles y permisos
- Registro de auditoría

## Requisitos

- Python 3.8+
- PostgreSQL
- Node.js y npm (para el frontend)

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd sistema-expedientes-gmitre
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear archivo `.env` con:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_db
JWT_SECRET_KEY=tu_clave_secreta
```

5. Inicializar la base de datos:
```bash
flask db upgrade
```

## Configuración en Red Local

Para usar el sistema en múltiples computadoras en la misma red:

1. En la PC servidor:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear usuario administrador
python create_admin.py

# Configurar red
python setup_network.py

# Iniciar backend
python app.py

# Iniciar frontend (en otra terminal)
cd frontend
npm install
npm start
```

2. En las PCs cliente:
- Abrir el navegador
- Acceder a `http://[IP-SERVIDOR]:3000`
- Iniciar sesión con:
  - Usuario: admin
  - Contraseña: admin123

## Notas de Seguridad
- Cambiar la contraseña del administrador después del primer inicio de sesión
- Configurar el firewall para permitir conexiones a los puertos 5000 y 3000
- Asegurarse de que todas las PCs estén en la misma red local
- No exponer el sistema directamente a Internet sin configurar HTTPS

## Uso

1. Iniciar el servidor:
```bash
python app.py
```

2. Acceder a la aplicación en `http://localhost:5000`

## Estructura de Directorios

```
sistema-expedientes-gmitre/
├── app.py              # Aplicación principal
├── routes.py           # Rutas de la API
├── auth.py             # Autenticación
├── models/             # Modelos de datos
├── static/             # Archivos estáticos
├── templates/          # Plantillas
└── requirements.txt    # Dependencias
```

## Respaldo y Restauración

- Para crear un respaldo: Acceder a `/api/backup`
- Para restaurar: Usar la interfaz de administración

## Seguridad

- Autenticación JWT
- Roles: Administrador y Consultor
- Registro de todas las acciones
- Encriptación de contraseñas

## Soporte

Para soporte técnico, contactar a [correo-de-soporte]
