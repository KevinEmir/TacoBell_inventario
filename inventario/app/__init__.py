from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from app.config import Config  # asegúrate de importar tu clase Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from .routes.categorias import categorias_bp
    app.register_blueprint(categorias_bp)

    # Crear tablas si no existen (solo en desarrollo)
    with app.app_context():
        db.create_all()

    # 👇 MOVER AQUÍ el context_processor
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}

    return app
