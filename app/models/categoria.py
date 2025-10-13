from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from .. import db
from datetime import datetime

class Categoria(db.Model):
    __tablename__ = "Categorias"
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False, unique=True)
    Descripcion = db.Column(db.Text, nullable=True)
    Activo = db.Column(db.Boolean, nullable=False, default=True)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Categoria {self.Nombre}>"
