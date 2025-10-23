@echo off
cd /d "C:\Users\Kevin\Documents\GitHub\TacoBell_inventario"

"venv\Scripts\python.exe" - <<END
from app import create_app
from app.forms.exporter import export_low_stock

app = create_app()

with app.app_context():
    export_low_stock()
END

pause
