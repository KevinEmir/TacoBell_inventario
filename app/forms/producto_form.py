from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductoForm(FlaskForm):
    """Formulario para crear o editar productos, alineado con la BD."""

    # === Campos básicos ===
    Nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre del producto es obligatorio."),
            Length(max=150, message="El nombre no puede tener más de 150 caracteres.")
        ]
    )

    Descripcion = TextAreaField(
        "Descripción",
        validators=[
            Optional(),
            Length(max=500, message="La descripción no puede tener más de 500 caracteres.")
        ]
    )

    CodigoSKU = StringField(
        "Código SKU",
        validators=[
            DataRequired(message="Debe ingresar el código SKU."),
            Length(max=50, message="El código SKU no puede tener más de 50 caracteres.")
        ]
    )

    CantidadActual = DecimalField(
        "Cantidad actual",
        validators=[
            Optional(),
            NumberRange(min=0, message="La cantidad no puede ser negativa.")
        ]
    )

    UnidadMedida = StringField(
        "Unidad de medida",
        validators=[
            DataRequired(message="Debe especificar la unidad de medida."),
            Length(max=20, message="La unidad no puede tener más de 20 caracteres.")
        ]
    )

    StockMinimo = DecimalField(
        "Stock mínimo",
        validators=[
            Optional(),
            NumberRange(min=0, message="El stock mínimo no puede ser negativo.")
        ]
    )

    PrecioUnitario = DecimalField(
        "Precio unitario",
        validators=[
            Optional(),
            NumberRange(min=0, message="El precio unitario no puede ser negativo.")
        ]
    )

    # === Relaciones ===
    CategoriaId = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    ProveedorId = SelectField("Proveedor", coerce=int, validators=[DataRequired()])

    # === Estado ===
    Activo = BooleanField("Activo", default=True)

    # === Botón de envío ===
    submit = SubmitField("Guardar")
