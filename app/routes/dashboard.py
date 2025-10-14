# app/routes/dashboard.py

from flask import Blueprint, render_template
from .. import db
from ..models.producto import Producto
from ..models.movimiento import Movimiento
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates", url_prefix="/")

@dashboard_bp.route("/", methods=["GET"])
def index():
    """
    Página principal /dashboard:
    Calcula métricas y las pasa a la plantilla.
    """

    # 1) Total productos activos
    # Se asume que Producto tiene atributo Activo (bit) y Nombre/CantidadActual/StockMinimo/PrecioUnitario.
    total_productos_activos = db.session.query(func.count(Producto.Id)).filter(Producto.Activo == True).scalar()

    # 2) Productos con stock bajo (CantidadActual <= StockMinimo) y activos
    productos_bajo_stock_q = db.session.query(Producto).filter(
        Producto.Activo == True,
        Producto.CantidadActual <= Producto.StockMinimo
    ).order_by(Producto.CantidadActual.asc())

    productos_bajo_stock = productos_bajo_stock_q.limit(10).all()  # lista corta para mostrar

    # contar cuantos hay (puede ser mayor que 10)
    count_bajo_stock = productos_bajo_stock_q.count()

    # 3) Productos sin stock (CantidadActual = 0) y activos
    productos_sin_stock = db.session.query(func.count(Producto.Id)).filter(
        Producto.Activo == True,
        Producto.CantidadActual == 0
    ).scalar()

    # 4) Valor total del inventario: sum(CantidadActual * PrecioUnitario) para productos activos
    # Usamos func.sum con la expresión aritmética
    valor_total = db.session.query(func.sum(Producto.CantidadActual * Producto.PrecioUnitario)).filter(
        Producto.Activo == True
    ).scalar() or 0

    # 5) Últimos 5 movimientos (ordenados por FechaCreacion desc)
    ultimos_movimientos = Movimiento.query.order_by(Movimiento.FechaCreacion.desc()).limit(5).all()

    # Pasamos todo a la plantilla
    return render_template(
        "dashboard.html",
        total_productos_activos=total_productos_activos,
        count_bajo_stock=count_bajo_stock,
        productos_bajo_stock=productos_bajo_stock,
        productos_sin_stock=productos_sin_stock,
        valor_total=valor_total,
        ultimos_movimientos=ultimos_movimientos
    )
