from openpyxl import Workbook
from app.models.producto import Producto
import os

def export_low_stock():
    productos = Producto.query.filter(
        (Producto.CantidadActual <= Producto.StockMinimo) |
        (Producto.CantidadActual == 0),
        Producto.Activo == True
    ).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Low Stock"
    ws.append(["ID", "Name", "Current Qty", "Min Stock", "Unit", "Unit Price"])

    for p in productos:
        ws.append([
            p.Id,
            p.Nombre,
            float(p.CantidadActual or 0),
            float(p.StockMinimo or 0),
            p.UnidadMedida,
            float(p.PrecioUnitario or 0)
        ])

    # 📁 Ruta local de OneDrive
    folder = r"C:\Users\Kevin\OneDrive - Inversiones TB S.A resco brands\TacoBell_inventario\stock_bajo"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "low_stock.xlsx")

    wb.save(path)
    print(f"✅ Archivo exportado en: {path}")
    print(f"📂 Carpeta actual del script: {os.getcwd()}")
    return path
