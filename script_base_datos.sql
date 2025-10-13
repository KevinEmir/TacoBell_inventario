from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models.movimiento import Movimiento
from ..models.producto import Producto
from sqlalchemy.exc import IntegrityError

# Blueprint con su prefijo y carpeta de templates
movimientos_bp = Blueprint("movimientos", __name__, template_folder="templates", url_prefix="/movimientos")

# --------------------------------------------------------------------
# LISTAR MOVIMIENTOS
# --------------------------------------------------------------------
@movimientos_bp.route("/", methods=["GET"])
def lista():
    q = request.args.get("q", "")
    if q:
        movimientos = Movimiento.query.filter(Movimiento.Tipo.ilike(f"%{q}%")).order_by(Movimiento.FechaCreacion.desc()).all()
    else:
        movimientos = Movimiento.query.order_by(Movimiento.FechaCreacion.desc()).all()
    return render_template("movimientos/lista.html", movimientos=movimientos, q=q)

# --------------------------------------------------------------------
# CREAR MOVIMIENTO
# --------------------------------------------------------------------
@movimientos_bp.route("/crear", methods=["GET", "POST"])
def crear():
    productos = Producto.query.all()  # Para desplegar lista de productos
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip().lower()
        cantidad = request.form.get("cantidad", "").strip()
        motivo = request.form.get("motivo", "").strip()
        notas = request.form.get("notas", "").strip()
        usuario = request.form.get("usuario", "Sistema").strip()
        producto_id = request.form.get("producto_id")

        # Validaciones básicas
        if not tipo or not cantidad or not producto_id:
            flash("Tipo, cantidad y producto son campos obligatorios.", "danger")
            return render_template("movimientos/form.html", accion="Registrar", movimiento={}, productos=productos)

        # Crear objeto Movimiento
        nuevo = Movimiento(
            Tipo=tipo,
            Cantidad=cantidad,
            Motivo=motivo,
            Notas=notas,
            Usuario=usuario,
            ProductoId=producto_id
        )

        db.session.add(nuevo)
        try:
            db.session.commit()
            flash("Movimiento registrado correctamente.", "success")
            return redirect(url_for("movimientos.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Error al registrar el movimiento. Intenta nuevamente.", "warning")
            return render_template("movimientos/form.html", accion="Registrar", movimiento=nuevo, productos=productos)

    return render_template("movimientos/form.html", accion="Registrar", movimiento={}, productos=productos)

# --------------------------------------------------------------------
# EDITAR MOVIMIENTO
# --------------------------------------------------------------------
@movimientos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    movimiento = Movimiento.query.get_or_404(id)
    productos = Producto.query.all()

    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip().lower()
        cantidad = request.form.get("cantidad", "").strip()
        motivo = request.form.get("motivo", "").strip()
        notas = request.form.get("notas", "").strip()
        usuario = request.form.get("usuario", "Sistema").strip()
        producto_id = request.form.get("producto_id")

        if not tipo or not cantidad or not producto_id:
            flash("Tipo, cantidad y producto son campos obligatorios.", "danger")
            return render_template("movimientos/form.html", accion="Editar", movimiento=movimiento, productos=productos)

        movimiento.Tipo = tipo
        movimiento.Cantidad = cantidad
        movimiento.Motivo = motivo
        movimiento.Notas = notas
        movimiento.Usuario = usuario
        movimiento.ProductoId = producto_id

        try:
            db.session.commit()
            flash("Movimiento actualizado correctamente.", "success")
            return redirect(url_for("movimientos.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Error al actualizar el movimiento.", "warning")
            return render_template("movimientos/form.html", accion="Editar", movimiento=movimiento, productos=productos)

    return render_template("movimientos/form.html", accion="Editar", movimiento=movimiento, productos=productos)

# --------------------------------------------------------------------
# ELIMINAR MOVIMIENTO (LÓGICO O FÍSICO)
# --------------------------------------------------------------------
@movimientos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    movimiento = Movimiento.query.get_or_404(id)
    db.session.delete(movimiento)
    db.session.commit()
    flash("Movimiento eliminado correctamente.", "info")
    return redirect(url_for("movimientos.lista"))
