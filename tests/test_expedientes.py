import pytest
from app import db
from models import Expediente

def test_crear_expediente(client, auth_headers):
    response = client.post('/api/expedientes', json={
        'numero': 'EXP-2023-001',
        'descripcion': 'Expediente de prueba',
        'color': 'Azul Pastel',
        'estado': 'Abierto',
        'monto': 1000.0
    }, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json['mensaje'] == 'Expediente creado exitosamente'
    
    expediente = Expediente.query.filter_by(numero='EXP-2023-001').first()
    assert expediente is not None
    assert expediente.descripcion == 'Expediente de prueba'

def test_buscar_expedientes(client, auth_headers):
    # Crear expediente de prueba
    expediente = Expediente(
        numero='EXP-2023-002',
        descripcion='Expediente de búsqueda',
        color='Verde Pastel',
        estado='Abierto',
        monto=2000.0
    )
    db.session.add(expediente)
    db.session.commit()
    
    response = client.get('/api/expedientes/buscar', query_string={
        'descripcion': 'búsqueda',
        'monto_min': 1000,
        'monto_max': 3000
    }, headers=auth_headers)
    
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['numero'] == 'EXP-2023-002'

def test_actualizar_expediente(client, auth_headers):
    # Crear expediente de prueba
    expediente = Expediente(
        numero='EXP-2023-003',
        descripcion='Expediente original',
        color='Rojo Pastel',
        estado='Abierto',
        monto=3000.0
    )
    db.session.add(expediente)
    db.session.commit()
    
    response = client.put(f'/api/expedientes/{expediente.id}', json={
        'descripcion': 'Expediente modificado',
        'estado': 'Cerrado'
    }, headers=auth_headers)
    
    assert response.status_code == 200
    
    expediente_actualizado = Expediente.query.get(expediente.id)
    assert expediente_actualizado.descripcion == 'Expediente modificado'
    assert expediente_actualizado.estado == 'Cerrado'

def test_eliminar_expediente(client, auth_headers):
    # Crear expediente de prueba
    expediente = Expediente(
        numero='EXP-2023-004',
        descripcion='Expediente a eliminar',
        color='Negro',
        estado='Abierto',
        monto=4000.0
    )
    db.session.add(expediente)
    db.session.commit()
    
    response = client.delete(f'/api/expedientes/{expediente.id}', headers=auth_headers)
    
    assert response.status_code == 200
    assert Expediente.query.get(expediente.id) is None
