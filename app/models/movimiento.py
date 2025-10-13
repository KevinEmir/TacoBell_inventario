from app import db
from datetime import datetime

class Movimiento(db.Model):
    __tablename__ = 'Movimientos'

    Id = db.Column(db.Integer, primary_key=True)
    ProductoId = db.Column(db.Integer, db.ForeignKey('Productos.Id'), nullable=False)

    # Tipo: 'entrada' o 'salida'
    Tipo = db.Column(db.String(20), nullable=False)

    # Cantidad del movimiento
    Cantidad = db.Column(db.Numeric(10, 2), nullable=False)

    # Campos adicionales
    Motivo = db.Column(db.String(200))
    Notas = db.Column(db.Text)
    Usuario = db.Column(db.String(100), default='Sistema')

    # Fecha del movimiento
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el producto
    producto = db.relationship('Producto', backref='movimientos', lazy=True)

    def __repr__(self):
        return f"<Movimiento {self.Id} - {self.Tipo} ({self.Cantidad})>"
