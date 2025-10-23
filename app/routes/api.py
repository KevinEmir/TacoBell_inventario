from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/stock_bajo', methods=['GET'])
def stock_bajo():
    # Importación local para evitar el ciclo con app/__init__.py
    from app.models.producto import Producto  

    productos = Producto.query.filter(
        (Producto.CantidadActual <= Producto.StockMinimo) |
        (Producto.CantidadActual == 0),
        Producto.Activo == True
    ).all()

    resultado = [
        {
            'Id': p.Id,
            'Nombre': p.Nombre,
            'CantidadActual': float(p.CantidadActual or 0),
            'StockMinimo': float(p.StockMinimo or 0),
            'UnidadMedida': p.UnidadMedida,
            'PrecioUnitario': float(p.PrecioUnitario or 0)
        }
        for p in productos
    ]

    return jsonify(resultado)
