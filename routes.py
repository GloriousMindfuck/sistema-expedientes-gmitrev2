from flask import jsonify, request
from app import app, db, Usuario, Expediente, Log
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
from datetime import datetime
import json

@app.route('/api/expedientes', methods=['POST'])
@jwt_required()
def crear_expediente():
    data = request.get_json()
    usuario_actual = get_jwt_identity()
    
    nuevo_expediente = Expediente(
        numero=data['numero'],
        descripcion=data['descripcion'],
        color=data['color'],
        color_bibliorato=data.get('color_bibliorato'),
        estado=data['estado'],
        monto=data['monto'],
        created_by=usuario_actual
    )
    
    db.session.add(nuevo_expediente)
    
    # Registrar en log
    log = Log(
        usuario_id=usuario_actual,
        accion='crear_expediente',
        detalles=f'Expediente {data["numero"]} creado'
    )
    db.session.add(log)
    
    db.session.commit()
    return jsonify({'mensaje': 'Expediente creado exitosamente'}), 201

@app.route('/api/expedientes/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_expediente(id):
    data = request.get_json()
    expediente = Expediente.query.get_or_404(id)
    
    for key, value in data.items():
        if hasattr(expediente, key):
            setattr(expediente, key, value)
    
    db.session.commit()
    return jsonify({'mensaje': 'Expediente actualizado exitosamente'})

@app.route('/api/expedientes/buscar', methods=['GET'])
@jwt_required()
def buscar_expedientes():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    descripcion = request.args.get('descripcion')
    monto_min = request.args.get('monto_min')
    monto_max = request.args.get('monto_max')
    
    query = Expediente.query
    
    if fecha_desde and fecha_hasta:
        query = query.filter(
            Expediente.fecha_pago.between(fecha_desde, fecha_hasta)
        )
    
    if descripcion:
        query = query.filter(Expediente.descripcion.ilike(f'%{descripcion}%'))
    
    if monto_min:
        query = query.filter(Expediente.monto >= float(monto_min))
    
    if monto_max:
        query = query.filter(Expediente.monto <= float(monto_max))
    
    expedientes = query.all()
    return jsonify([{
        'id': e.id,
        'numero': e.numero,
        'descripcion': e.descripcion,
        'color': e.color,
        'estado': e.estado,
        'monto': e.monto,
        'fecha_pago': e.fecha_pago.isoformat() if e.fecha_pago else None
    } for e in expedientes])

@app.route('/api/expedientes/exportar', methods=['GET'])
@jwt_required()
def exportar_expedientes():
    # Similar a buscar_expedientes pero retorna un archivo Excel
    expedientes = Expediente.query.all()
    df = pd.DataFrame([{
        'Número': e.numero,
        'Descripción': e.descripcion,
        'Color': e.color,
        'Estado': e.estado,
        'Monto': e.monto,
        'Fecha de Pago': e.fecha_pago
    } for e in expedientes])
    
    # Guardar a Excel
    excel_file = 'expedientes_export.xlsx'
    df.to_excel(excel_file, index=False)
    return send_file(excel_file, as_attachment=True)

@app.route('/api/backup', methods=['GET'])
@jwt_required()
def backup_data():
    expedientes = Expediente.query.all()
    data = [{
        'numero': e.numero,
        'descripcion': e.descripcion,
        'color': e.color,
        'color_bibliorato': e.color_bibliorato,
        'estado': e.estado,
        'monto': e.monto,
        'fecha_creacion': e.fecha_creacion.isoformat(),
        'fecha_pago': e.fecha_pago.isoformat() if e.fecha_pago else None
    } for e in expedientes]
    
    return jsonify(data)
