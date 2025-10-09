from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.categoria import Categoria
from sqlalchemy.exc import IntegrityError

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/', methods=['GET'])
def lista():
    q = request.args.get('q', '').strip()
    if q:
        categorias = Categoria.query.filter(Categoria.Nombre.ilike(f"%{q}%")).order_by(Categoria.Nombre).all()
    else:
        categorias = Categoria.query.order_by(Categoria.Nombre).all()
    return render_template('categorias/lista.html', categorias=categorias, q=q)

@categorias_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return render_template('categorias/form.html', accion='Crear', categoria={})
        nueva = Categoria(Nombre=nombre, Descripcion=descripcion)
        db.session.add(nueva)
        try:
            db.session.commit()
            flash('Categoría creada correctamente.', 'success')
            return redirect(url_for('categorias.lista'))
        except IntegrityError:
            db.session.rollback()
            flash('Ya existe una categoría con ese nombre.', 'warning')
            return render_template('categorias/form.html', accion='Crear', categoria={'Nombre': nombre, 'Descripcion': descripcion})
    return render_template('categorias/form.html', accion='Crear', categoria={})

@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return render_template('categorias/form.html', accion='Editar', categoria=categoria)
        categoria.Nombre = nombre
        categoria.Descripcion = descripcion
        db.session.commit()
        flash('Categoría actualizada correctamente.', 'success')
        return redirect(url_for('categorias.lista'))
    return render_template('categorias/form.html', accion='Editar', categoria=categoria)

@categorias_bp.route('/eliminar/<int:id>', methods=['POST','GET'])
def eliminar(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada con éxito.', 'success')
    return redirect(url_for('categorias.lista'))
