# RoxHome CRM

CRM/ERP ligero en Streamlit para operación comercial y técnica de RoxHome.

## Requisitos
- Python 3.11+

## Instalación
```bash
cd roxhome_crm
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Ejecución
```bash
streamlit run app.py
```

## Usuario inicial
- Email: `admin@roxhome.local`
- Password: `admin123`
- Rol: `Administrador`

## Módulos principales
- Dashboard de KPI y gráficos.
- Leads con conversión a contacto/cuenta/trato.
- Presupuestos con cálculo de subtotal, descuento, IVA, total y aprobación a orden de venta.
- Órdenes de venta con creación de servicio técnico.
- Servicios técnicos con checklist.
- Facturas con estado automático por pago y vencimiento.
- Campañas, productos, técnicos, reportes, análisis.
- Importación/Exportación y backups.

## Exportación Excel
En **Importar/Exportar Excel** usa **Exportar toda la base a Excel**.
Se genera en `exports/roxhome_crm_export_YYYYMMDD_HHMM.xlsx`.

## Backup
En **Importar/Exportar Excel** usa **Crear backup de SQLite**.
Se genera en `backups/roxhome_backup_YYYYMMDD_HHMM.db`.
