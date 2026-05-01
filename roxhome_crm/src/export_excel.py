from datetime import datetime
from pathlib import Path
import pandas as pd
from sqlalchemy import inspect
from .config import EXPORT_DIR, COMPANY_NAME


def export_all(engine):
    name = EXPORT_DIR / f"roxhome_crm_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    inspector = inspect(engine)
    with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
        for t in inspector.get_table_names():
            df = pd.read_sql_table(t, engine)
            df.to_excel(writer, sheet_name=t[:31], index=False)
    return name


def export_quote_excel(quote, items_df, client_name='Cliente'):
    file_path = EXPORT_DIR / f"presupuesto_{quote.presupuesto_codigo}.xlsx"
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        workbook = writer.book
        ws = workbook.add_worksheet('Presupuesto')
        writer.sheets['Presupuesto'] = ws

        fmt_title = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#7A1230'})
        fmt_head = workbook.add_format({'bold': True, 'bg_color': '#1E2F4F', 'font_color': 'white'})
        fmt_money = workbook.add_format({'num_format': '$#,##0.00'})

        ws.write('A1', COMPANY_NAME, fmt_title)
        ws.write('A3', 'Presupuesto #'); ws.write('B3', quote.presupuesto_codigo)
        ws.write('A4', 'Fecha'); ws.write('B4', str(quote.fecha))
        ws.write('A5', 'Cliente'); ws.write('B5', client_name)
        ws.write('A6', 'Validez'); ws.write('B6', str(quote.valido_hasta))

        start = 8
        headers = ['Descripción', 'Cantidad', 'Costo Unitario', 'Precio Unitario', 'Descuento', 'Subtotal']
        for i, h in enumerate(headers):
            ws.write(start, i, h, fmt_head)
        for r, row in items_df.iterrows():
            ws.write(start + 1 + r, 0, row['descripcion'])
            ws.write(start + 1 + r, 1, row['cantidad'])
            ws.write(start + 1 + r, 2, row['costo_unitario'], fmt_money)
            ws.write(start + 1 + r, 3, row['precio_unitario'], fmt_money)
            ws.write(start + 1 + r, 4, row['descuento'], fmt_money)
            ws.write(start + 1 + r, 5, row['subtotal'], fmt_money)

        row_end = start + 2 + len(items_df)
        ws.write(row_end, 4, 'Subtotal'); ws.write(row_end, 5, quote.subtotal, fmt_money)
        ws.write(row_end + 1, 4, 'Descuento'); ws.write(row_end + 1, 5, quote.descuento, fmt_money)
        ws.write(row_end + 2, 4, 'IVA'); ws.write(row_end + 2, 5, quote.iva, fmt_money)
        ws.write(row_end + 3, 4, 'Total'); ws.write(row_end + 3, 5, quote.total, fmt_money)
        ws.write(row_end + 5, 0, 'Condiciones'); ws.write(row_end + 5, 1, quote.condiciones or '')
        ws.write(row_end + 6, 0, 'Observaciones'); ws.write(row_end + 6, 1, quote.notas or '')

        ws.set_column('A:A', 40)
        ws.set_column('B:F', 16)
    return file_path
