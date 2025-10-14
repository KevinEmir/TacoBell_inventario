from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class MovimientoForm(FlaskForm):
    """Formulario para registrar o editar movimientos."""

    producto_id = SelectField("Producto", coerce=int, validators=[DataRequired()])
    tipo = SelectField(
        "Tipo de movimiento",
        choices=[("entrada", "Entrada"), ("salida", "Salida")],
        validators=[DataRequired()],
    )
    cantidad = DecimalField("Cantidad", validators=[DataRequired(), NumberRange(min=0.01)])
    
    # 🔹 AHORA ES SELECTFIELD (antes era TextAreaField)
    motivo = SelectField("Motivo", choices=[], validators=[DataRequired()])
    
    notas = TextAreaField("Notas")
    submit = SubmitField("Guardar")
