from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.proveedores import Proveedor
from sqlalchemy.exc import IntegrityError

proveedores_bp = Blueprint('proveedores', __name__, template_folder='../../templates/proveedores')

@proveedores_bp.route("/", methods=["GET"])
def lista():
    q = request.args.get("q", "").strip()
    activo = request.args.get("activo", "")

    # Consulta base ordenada por Id descendente
    consulta = Proveedor.query.order_by(Proveedor.Id.desc())

    # Filtro por nombre, contacto o email
    if q:
        consulta = consulta.filter(
            (Proveedor.nombre.ilike(f"%{q}%")) |
            (Proveedor.contacto.ilike(f"%{q}%")) |
            (Proveedor.email.ilike(f"%{q}%"))
        )

    # Filtro por estado (activo/inactivo)
    if activo in ["0", "1"]:
        consulta = consulta.filter(Proveedor.activo == (activo == "1"))

    proveedores = consulta.all()

    return render_template(
        "proveedores/lista.html",
        proveedores=proveedores,
        q=q,
        activo=activo
    )




@proveedores_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    """Crear un nuevo proveedor"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        contacto = request.form.get('contacto', '').strip() or None
        telefono = request.form.get('telefono', '').strip() or None
        email = request.form.get('email', '').strip() or None
        direccion = request.form.get('direccion', '').strip() or None

        errors = []
        if not nombre:
            errors.append("El nombre es obligatorio.")
        if email and '@' not in email:
            errors.append("Email inválido.")

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('proveedores/form.html', proveedor=None, form=request.form)

        proveedor = Proveedor(
            nombre=nombre,
            contacto=contacto,
            telefono=telefono,
            email=email,
            direccion=direccion
        )

        try:
            db.session.add(proveedor)
            db.session.commit()
            flash("Proveedor creado correctamente.", "success")
            return redirect(url_for('proveedores.lista'))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe un proveedor con ese nombre.", "danger")
            return render_template('proveedores/form.html', proveedor=None, form=request.form)

    return render_template('proveedores/form.html', proveedor=None, form={})


@proveedores_bp.route('/editar/<int:proveedor_id>', methods=['GET', 'POST'])
def editar(proveedor_id):
    """Editar un proveedor existente"""
    proveedor = Proveedor.query.get_or_404(proveedor_id)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        contacto = request.form.get('contacto', '').strip() or None
        telefono = request.form.get('telefono', '').strip() or None
        email = request.form.get('email', '').strip() or None
        direccion = request.form.get('direccion', '').strip() or None

        errors = []
        if not nombre:
            errors.append("El nombre es obligatorio.")
        if email and '@' not in email:
            errors.append("Email inválido.")

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('proveedores/form.html', proveedor=proveedor, form=request.form)

        proveedor.nombre = nombre
        proveedor.contacto = contacto
        proveedor.telefono = telefono
        proveedor.email = email
        proveedor.direccion = direccion

        try:
            db.session.commit()
            flash("Proveedor actualizado correctamente.", "success")
            return redirect(url_for('proveedores.lista'))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe un proveedor con ese nombre.", "danger")
            return render_template('proveedores/form.html', proveedor=proveedor, form=request.form)

    return render_template('proveedores/form.html', proveedor=proveedor, form={})


@proveedores_bp.route('/eliminar/<int:proveedor_id>', methods=['POST'])
def eliminar(proveedor_id):
    """Eliminar (desactivar) proveedor - eliminación lógica"""
    proveedor = Proveedor.query.get_or_404(proveedor_id)
    proveedor.activo = False
    db.session.commit()
    flash("Proveedor desactivado correctamente.", "warning")
    return redirect(url_for('proveedores.lista'))


@proveedores_bp.route("/reactivar/<int:proveedor_id>", methods=["POST"])
def reactivar(proveedor_id):
    """Reactivar proveedor desactivado"""
    proveedor = Proveedor.query.get_or_404(proveedor_id)
    proveedor.activo = True
    db.session.commit()
    flash("Proveedor reactivado correctamente.", "success")
    return redirect(url_for("proveedores.lista"))
