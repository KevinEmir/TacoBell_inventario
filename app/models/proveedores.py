# app/models/proveedor.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from datetime import datetime
from app import db  # 'db' es la instancia de SQLAlchemy creada en app/__init__.py

class Proveedor(db.Model):
    """
    Modelo Proveedor:
    - id: clave primaria
    - nombre: nombre del proveedor (obligatorio)
    - contacto: persona de contacto (opcional)
    - telefono: teléfono (opcional)
    - email: correo electrónico (opcional)
    - direccion: dirección física (opcional)
    - activo: eliminación lógica (booleano)
    - fecha_creacion: marca temporal de creación
    """

    __tablename__ = 'Proveedores'  # nombre de la tabla en la BD

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Proveedor id={self.id} nombre={self.nombre}>"
