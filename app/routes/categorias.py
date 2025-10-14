from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models.categoria import Categoria
from sqlalchemy.exc import IntegrityError

categorias_bp = Blueprint("categorias", __name__, template_folder="templates", url_prefix="/categorias")

@categorias_bp.route("/", methods=["GET"])
def lista():
    q = request.args.get("q", "")
    if q:
        categorias = Categoria.query.filter(Categoria.Nombre.ilike(f"%{q}%")).order_by(Categoria.Nombre).all()
    else:
        categorias = Categoria.query.order_by(Categoria.Id.asc()).all()

    return render_template("categorias/lista.html", categorias=categorias, q=q)

@categorias_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return render_template("categorias/form.html", accion="Crear", categoria={})
        nueva = Categoria(Nombre=nombre, Descripcion=descripcion)
        db.session.add(nueva)
        try:
            db.session.commit()
            flash("Categoría creada correctamente.", "success")
            return redirect(url_for("categorias.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe una categoría con ese nombre.", "warning")
            return render_template("categorias/form.html", accion="Crear", categoria={"Nombre": nombre, "Descripcion": descripcion})
    return render_template("categorias/form.html", accion="Crear", categoria={})

@categorias_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return render_template("categorias/form.html", accion="Editar", categoria=categoria)
        categoria.Nombre = nombre
        categoria.Descripcion = descripcion
        try:
            db.session.commit()
            flash("Categoría actualizada.", "success")
            return redirect(url_for("categorias.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe otra categoría con ese nombre.", "warning")
            return render_template("categorias/form.html", accion="Editar", categoria=categoria)
    return render_template("categorias/form.html", accion="Editar", categoria=categoria)

@categorias_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    categoria = Categoria.query.get_or_404(id)
    # eliminación lógica
    categoria.Activo = False
    db.session.commit()
    flash("Categoría desactivada (eliminación lógica).", "info")
    return redirect(url_for("categorias.lista"))

@categorias_bp.route("/reactivar/<int:id>", methods=["POST"])
def reactivar(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.Activo = True
    db.session.commit()
    flash("Categoría reactivada correctamente.", "success")
    return redirect(url_for("categorias.lista"))
