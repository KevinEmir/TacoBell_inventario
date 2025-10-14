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
        movimientos = Movimiento.query.filter(Movimiento.Tipo.ilike(f"%{q}%")).order_by(Movimiento.FechaCreacion.desc()).all()
    else:
        movimientos = Movimiento.query.order_by(Movimiento.FechaCreacion.desc()).all()
    return render_template("movimientos/lista.html", movimientos=movimientos, q=q)


@movimientos_bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MovimientoForm()

    # Cargar productos activos
    productos = Producto.query.filter_by(Activo=True).order_by(Producto.Nombre).all()
    form.producto_id.choices = [(p.Id, p.Nombre) for p in productos]

    # Cargar motivos dinámicamente según el tipo seleccionado
    if form.tipo.data == "entrada":
        form.motivo.choices = [("Compra", "Compra"), ("Devolución", "Devolución"), ("Ajuste", "Ajuste")]
    elif form.tipo.data == "salida":
        form.motivo.choices = [("Producción", "Producción"), ("Merma", "Merma"), ("Vencido", "Vencido")]
    else:
        form.motivo.choices = []

    # POST: guardar movimiento
    if request.method == "POST" and form.validate_on_submit():
        nuevo = Movimiento(
            ProductoId=form.producto_id.data,
            Tipo=form.tipo.data.lower(),
            Cantidad=form.cantidad.data,
            Motivo=form.motivo.data,
            Notas=form.notas.data,
            Usuario="Sistema",
        )

        # Actualizar stock del producto
        producto = Producto.query.get(form.producto_id.data)
        if nuevo.Tipo == "entrada":
            producto.CantidadActual += nuevo.Cantidad
        elif nuevo.Tipo == "salida":
            if producto.CantidadActual - nuevo.Cantidad < 0:
                flash("Error: No hay stock suficiente para registrar esta salida.", "danger")
                return render_template("movimientos/form.html", accion="Registrar", form=form)
            producto.CantidadActual -= nuevo.Cantidad

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
    productos = Producto.query.filter_by(Activo=True).order_by(Producto.Nombre).all()

    form = MovimientoForm()
    form.producto_id.choices = [(p.Id, p.Nombre) for p in productos]

    # Cargar motivos según tipo
    if movimiento.Tipo == "entrada":
        form.motivo.choices = [("Compra", "Compra"), ("Devolución", "Devolución"), ("Ajuste", "Ajuste")]
    else:
        form.motivo.choices = [("Producción", "Producción"), ("Merma", "Merma"), ("Vencido", "Vencido")]

    # Prellenar datos
    if request.method == "GET":
        form.producto_id.data = movimiento.ProductoId
        form.tipo.data = movimiento.Tipo
        form.cantidad.data = movimiento.Cantidad
        form.motivo.data = movimiento.Motivo
        form.notas.data = movimiento.Notas

    if request.method == "POST" and form.validate_on_submit():
        movimiento.ProductoId = form.producto_id.data
        movimiento.Tipo = form.tipo.data
        movimiento.Cantidad = form.cantidad.data
        movimiento.Motivo = form.motivo.data
        movimiento.Notas = form.notas.data

        try:
            db.session.commit()
            flash("Movimiento actualizado correctamente.", "success")
            return redirect(url_for("movimientos.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Error al actualizar el movimiento.", "warning")

    return render_template("movimientos/form.html", accion="Editar", form=form, movimiento=movimiento)


@movimientos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    movimiento = Movimiento.query.get_or_404(id)
    movimiento.Activo = False  # eliminación lógica
    db.session.commit()
    flash("Movimiento desactivado correctamente.", "info")
    return redirect(url_for("movimientos.lista"))
