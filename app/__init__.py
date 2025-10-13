from flask import Flask,blueprints
from flask_sqlalchemy import SQLAlchemy
from config import Config

#Instancia global de SQLAlchemy
# 'SQLAlchemy' es el ORM (Object Relational Mapper)
# que permite trabajar con la base de datos usando clases Python
db = SQLAlchemy()


# Esta función crea y configura una instancia de Flask.
def create_app():
    flask_app = Flask(__name__)


    # Aquí Flask leerá las variables de la clase Config
    flask_app.config.from_object(Config)

    # Inicializar SQLAlchemy con la app
    db.init_app(flask_app)

    # Importar modelos
    # Esto asegura que SQLAlchemy conozca todas las clases

    import app.models.categoria
    import app.models.proveedores

    # Importar y registrar Blueprints (rutas)

    from .routes.categorias import categorias_bp
    flask_app.register_blueprint(categorias_bp, url_prefix="/categorias")

    from .routes.proveedores import proveedores_bp  
    flask_app.register_blueprint(proveedores_bp, url_prefix="/proveedores")


    #Crear las tablas en la base de datos (si no existen)
    with flask_app.app_context():
        db.create_all()

    # Devolver la app ya configurada
    return flask_app