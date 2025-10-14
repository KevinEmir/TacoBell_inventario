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
@productos_bp.route("/")
def lista():
    q = request.args.get("q", "").strip()

    consulta = (
        db.session.query(
            Producto,
            Categoria.Nombre.label("CategoriaNombre"),
            Proveedor.nombre.label("ProveedorNombre")
        )
        .join(Categoria, Producto.CategoriaId == Categoria.Id)
        .join(Proveedor, Producto.ProveedorId == Proveedor.Id)
        .order_by(Producto.Id.desc())
    )

    if q:
        consulta = consulta.filter(Producto.Nombre.ilike(f"%{q}%"))

    productos = consulta.all()

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
@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    """Formulario para editar un producto existente."""
    producto = Producto.query.get_or_404(id)
    form = ProductoForm()

    # Cargar listas desplegables
    form.CategoriaId.choices = [(c.Id, c.Nombre) for c in Categoria.query.all()]
    form.ProveedorId.choices = [(p.Id, p.nombre) for p in Proveedor.query.all()]


    # --- Prellenar valores del producto (solo en GET) ---
    if request.method == "GET":
        form.Nombre.data = producto.Nombre
        form.Descripcion.data = producto.Descripcion
        form.CodigoSKU.data = producto.CodigoSKU
        form.CantidadActual.data = producto.CantidadActual
        form.UnidadMedida.data = producto.UnidadMedida
        form.StockMinimo.data = producto.StockMinimo
        form.PrecioUnitario.data = producto.PrecioUnitario
        form.CategoriaId.data = producto.CategoriaId
        form.ProveedorId.data = producto.ProveedorId
        form.Activo.data = producto.Activo

    # --- Guardar cambios (POST) ---
    if request.method == "POST" and form.validate_on_submit():
        producto.Nombre = form.Nombre.data
        producto.Descripcion = form.Descripcion.data
        producto.CodigoSKU = form.CodigoSKU.data
        producto.CantidadActual = form.CantidadActual.data
        producto.UnidadMedida = form.UnidadMedida.data
        producto.StockMinimo = form.StockMinimo.data
        producto.PrecioUnitario = form.PrecioUnitario.data
        producto.CategoriaId = form.CategoriaId.data
        producto.ProveedorId = form.ProveedorId.data
        producto.Activo = form.Activo.data


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
