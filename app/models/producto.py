from app import db
from datetime import datetime

class Producto(db.Model):
    """
    Modelo que representa la tabla 'Productos' en la base de datos.
    Cada atributo de esta clase corresponde a una columna SQL.
    """

    __tablename__ = 'Productos'  # Asegura que SQLAlchemy use este nombre exacto de tabla

    # === Columnas principales ===
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(300), nullable=False)
    Descripcion = db.Column(db.Text, nullable=True)
    CodigoSKU = db.Column(db.String(100), nullable=True, unique=True)
    CantidadActual = db.Column(db.Numeric(10, 2), nullable=True)
    UnidadMedida = db.Column(db.String(40), nullable=True)
    StockMinimo = db.Column(db.Numeric(10, 2), nullable=True)
    PrecioUnitario = db.Column(db.Numeric(10, 2), nullable=True)

    # === Relaciones con otras tablas ===
    CategoriaId = db.Column(db.Integer, db.ForeignKey('Categorias.Id'), nullable=False)
    ProveedorId = db.Column(db.Integer, db.ForeignKey('Proveedores.Id'), nullable=False)

    # === Campos de estado y auditoría ===
    Activo = db.Column(db.Boolean, default=True)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    FechaActualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # === Relaciones ORM para acceso directo a los objetos relacionados ===
    categoria = db.relationship('Categoria', backref='productos', lazy=True)
    proveedor = db.relationship('Proveedor', backref='productos', lazy=True)

    def __repr__(self):
        """
        Método usado para representar el objeto como texto (útil para depuración).
        """
        return f"<Producto {self.Nombre}>"
