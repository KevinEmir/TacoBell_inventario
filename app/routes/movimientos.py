from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models.movimiento import Movimiento
from ..models.producto import Producto
from sqlalchemy.exc import IntegrityError
from app.forms.movimiento_form import MovimientoForm


# Blueprint con prefijo y carpeta de templates
movimientos_bp = Blueprint("movimientos", __name__, template_folder="templates", url_prefix="/movimientos")

@movimientos_bp.route("/", methods=["GET"])
def lista():
    q = request.args.get("q", "")
    if q:
        movimientos = Movimiento.query.filter(Movimiento.TipoMovimiento.ilike(f"%{q}%")).order_by(Movimiento.Fecha.desc()).all()
    else:
        movimientos = Movimiento.query.order_by(Movimiento.FechaCreacion.desc()).all()
    return render_template("movimientos/lista.html", movimientos=movimientos, q=q)

@movimientos_bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MovimientoForm()

    # Cargar productos activos para el select
    productos = Producto.query.filter_by(Activo=True).order_by(Producto.Nombre).all()
    form.producto_id.choices = [(p.Id, p.Nombre) for p in productos]

    if request.method == "POST" and form.validate_on_submit():
        # Crear movimiento
        nuevo = Movimiento(
            ProductoId=form.producto_id.data,
            Tipo=form.tipo.data.lower(),
            Cantidad=form.cantidad.data,
            Motivo=form.motivo.data,
            Notas=form.notas.data,
            Usuario="Sistema",
        )

        # Buscar el producto afectado
        producto = Producto.query.get(form.producto_id.data)

        # --- Actualizar stock según tipo ---
        if nuevo.Tipo == "entrada":
            producto.CantidadActual += nuevo.Cantidad
        elif nuevo.Tipo == "salida":
            # Validar que no haya stock negativo
            if producto.CantidadActual - nuevo.Cantidad < 0:
                flash("Error: No hay stock suficiente para registrar esta salida.", "danger")
                return render_template("movimientos/form.html", accion="Registrar", form=form)
            producto.CantidadActual -= nuevo.Cantidad
        else:
            flash("Tipo de movimiento no válido.", "danger")
            return render_template("movimientos/form.html", accion="Registrar", form=form)

        # Guardar movimiento y actualizar producto
        try:
            db.session.add(nuevo)
            db.session.commit()
            flash("Movimiento registrado correctamente y stock actualizado.", "success")
            return redirect(url_for("movimientos.lista"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar el movimiento: {str(e)}", "danger")

    return render_template("movimientos/form.html", accion="Registrar", form=form)


@movimientos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    movimiento = Movimiento.query.get_or_404(id)
    productos = Producto.query.join(Proveedor).add_columns(Producto.Id, Producto.Nombre, Proveedor.nombre.label("proveedor")).all()


    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        cantidad = request.form.get("cantidad", "").strip()
        producto_id = request.form.get("producto_id")

        if not tipo or not cantidad or not producto_id:
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("movimientos/form.html", accion="Registrar", movimiento=movimiento, productos=productos)


        movimiento.Tipo = Tipo
        movimiento.Cantidad = cantidad
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

@movimientos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    movimiento = Movimiento.query.get_or_404(id)
    movimiento.Activo = False  # eliminación lógica
    db.session.commit()
    flash("Movimiento desactivado correctamente.", "info")
    return redirect(url_for("movimientos.lista"))
