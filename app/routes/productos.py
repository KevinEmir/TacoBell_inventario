from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.proveedores import Proveedor
from app.forms.producto_form import ProductoForm
from sqlalchemy.exc import IntegrityError

# ==============================
# CONFIGURACIÓN DEL BLUEPRINT
# ==============================
productos_bp = Blueprint(
    "productos",                # nombre interno del módulo
    __name__,                   # referencia del archivo actual
    template_folder="templates",# carpeta donde buscará las vistas HTML
    url_prefix="/productos"     # prefijo de las URLs (ej: /productos/crear)
)

# ==============================
# LISTAR PRODUCTOS
# ==============================
@productos_bp.route("/", methods=["GET"])
def lista():
    """Muestra la lista de productos con opción de búsqueda."""
    q = request.args.get("q", "").strip()

    if q:
        productos = Producto.query.filter(Producto.Nombre.ilike(f"%{q}%")).order_by(Producto.Nombre).all()
    else:
        productos = Producto.query.order_by(Producto.Nombre).all()

    return render_template("productos/lista.html", productos=productos, q=q)

# ==============================
# CREAR PRODUCTO
# ==============================
@productos_bp.route("/crear", methods=["GET", "POST"])
def crear():
    """Formulario para registrar un nuevo producto."""
    form = ProductoForm()

    # Cargar las opciones de categoría y proveedor desde la BD
    form.categoria_id.choices = [(c.Id, c.Nombre) for c in Categoria.query.all()]
    form.proveedor_id.choices = [(p.Id, p.nombre) for p in Proveedor.query.all()]


    if request.method == "POST" and form.validate_on_submit():
        nuevo = Producto(
            Nombre=form.nombre.data,
            Descripcion=form.descripcion.data,
            CodigoSKU=form.codigo_sku.data,
            CantidadActual=form.cantidad_actual.data,
            UnidadMedida=form.unidad_medida.data,
            StockMinimo=form.stock_minimo.data,
            PrecioUnitario=form.precio_unitario.data,
            CategoriaId=form.categoria_id.data,
            ProveedorId=form.proveedor_id.data,
            Activo=form.activo.data
        )
        db.session.add(nuevo)
        try:
            db.session.commit()
            flash("Producto creado correctamente.", "success")
            return redirect(url_for("productos.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe un producto con ese código SKU.", "warning")

    return render_template("productos/form.html", form=form, accion="Crear")

# ==============================
# EDITAR PRODUCTO
# ==============================
@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    """Formulario para editar un producto existente."""
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)

    # Cargar listas desplegables
    form.categoria_id.choices = [(c.Id, c.Nombre) for c in Categoria.query.all()]
    form.proveedor_id.choices = [(p.Id, p.nombre) for p in Proveedor.query.all()]

    if request.method == "POST" and form.validate_on_submit():
        producto.Nombre = form.nombre.data
        producto.Descripcion = form.descripcion.data
        producto.CodigoSKU = form.codigo_sku.data
        producto.CantidadActual = form.cantidad_actual.data
        producto.UnidadMedida = form.unidad_medida.data
        producto.StockMinimo = form.stock_minimo.data
        producto.PrecioUnitario = form.precio_unitario.data
        producto.CategoriaId = form.categoria_id.data
        producto.ProveedorId = form.proveedor_id.data
        producto.Activo = form.activo.data

        try:
            db.session.commit()
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("productos.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Error: ya existe un producto con ese SKU.", "danger")

    return render_template("productos/form.html", form=form, accion="Editar", producto=producto)

# ==============================
# ELIMINAR (LÓGICAMENTE) PRODUCTO
# ==============================
@productos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    """Desactiva un producto (eliminación lógica)."""
    producto = Producto.query.get_or_404(id)
    producto.Activo = False
    db.session.commit()
    flash("Producto desactivado con éxito.", "info")
    return redirect(url_for("productos.lista"))
