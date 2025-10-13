# Sistema de Gestión de Inventario — Módulo de Categorías (Día 1-2)

Este proyecto contiene la **estructura mínima** y un **módulo de Categorías** (CRUD)
implementado con **Flask + SQLAlchemy** y preparado para conectarse a **SQL Server**.

## Qué incluye
- Estructura del proyecto (app/, models/, routes/, templates/, static/)
- Conexión con SQLAlchemy (usar driver `pyodbc`)
- Modelo `Categoria` (creación, listado, edición, eliminación lógica)
- Plantillas Jinja2 para lista y formulario
- `script_base_datos.sql` incluido (proporcionado por el repositorio original)
- `requirements.txt` con dependencias

## Instrucciones rápidas
1. Instala dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # o venv\Scripts\activate en Windows
   pip install -r requirements.txt
   ```

2. Configura la URI de la base de datos en `config.py` o usando la variable de entorno `DATABASE_URL`.
   Ejemplo (SQL Server + ODBC Driver 17):
   ```
   mssql+pyodbc://<USER>:<PASSWORD>@<SERVER>/<DATABASE>?driver=ODBC+Driver+17+for+SQL+Server
   ```

   **Nota:** Reemplace espacios en el driver por `+` en la URI si su entorno lo requiere:
   `...driver=ODBC+Driver+17+for+SQL+Server`

3. Crea la base de datos y tablas ejecutando `script_base_datos.sql` en su instancia de SQL Server (SSMS o Azure Data Studio).

4. Ejecuta la aplicación:
   ```bash
   python run.py
   ```
   La app estará en `http://127.0.0.1:5000/` y el módulo de categorías en `/categorias`.

## Archivos importantes
- `script_base_datos.sql` — script de creación de la BD (ya incluido)
- `config.py` — configuración de la app y URI de la BD
- `run.py` — punto de entrada
- `app/models/categoria.py` — modelo Category
- `app/routes/categorias.py` — rutas CRUD

Si quieres, puedo:
- Añadir datos de prueba automáticos (seed)
- Añadir forms con Flask-WTF y validaciones de front-end
- Generar un `.bak` (requiere SQL Server local y no se puede hacer desde aquí)

