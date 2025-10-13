import os

# Configuración para SQLAlchemy. Preferible definir DATABASE_URL en variables de entorno.
# Ejemplo de URI para SQL Server:
# mssql+pyodbc://USER:PASSWORD@SERVER/DATABASE?driver=ODBC+Driver+17+for+SQL+Server

DATABASE_URL = "mssql+pyodbc://@localhost/InventarioRestaurante?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"





class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambie_esta_clave_para_produccion")
