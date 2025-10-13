from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductoForm(FlaskForm):
    """
    Formulario para crear o editar productos.
    Cada campo tiene validaciones que aseguran que los datos sean correctos
    antes de guardarlos en la base de datos.
    """

    # === Campos básicos ===
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre del producto es obligatorio."),
            Length(max=300, message="El nombre no puede tener más de 300 caracteres.")
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            Optional(),
            Length(max=500, message="La descripción no puede tener más de 500 caracteres.")
        ]
    )

    codigo_sku = StringField(
        "Código SKU",
        validators=[
            Optional(),
            Length(max=100, message="El código SKU no puede tener más de 100 caracteres.")
        ]
    )

    cantidad_actual = DecimalField(
        "Cantidad actual",
        validators=[
            DataRequired(message="Debe ingresar una cantidad."),
            NumberRange(min=0, message="La cantidad no puede ser negativa.")
        ]
    )

    unidad_medida = StringField(
        "Unidad de medida",
        validators=[
            DataRequired(message="Debe especificar la unidad de medida."),
            Length(max=40, message="La unidad no puede tener más de 40 caracteres.")
        ]
    )

    stock_minimo = DecimalField(
        "Stock mínimo",
        validators=[
            DataRequired(message="Debe ingresar un valor de stock mínimo."),
            NumberRange(min=0, message="El stock mínimo no puede ser negativo.")
        ]
    )

    precio_unitario = DecimalField(
        "Precio unitario",
        validators=[
            DataRequired(message="Debe ingresar el precio unitario."),
            NumberRange(min=0, message="El precio unitario no puede ser negativo.")
        ]
    )

    # === Relaciones ===
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    proveedor_id = SelectField("Proveedor", coerce=int, validators=[DataRequired()])

    # === Estado ===
    activo = BooleanField("Activo", default=True)

    # === Botón de envío ===
    submit = SubmitField("Guardar")
