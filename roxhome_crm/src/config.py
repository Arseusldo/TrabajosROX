from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / 'data'
EXPORT_DIR = BASE_DIR / 'exports'
BACKUP_DIR = BASE_DIR / 'backups'
UPLOADS_DIR = BASE_DIR / 'uploads'
DB_PATH = DATA_DIR / 'roxhome_crm.db'
DATABASE_URL = f"sqlite:///{DB_PATH}"

COMPANY_NAME = os.getenv('COMPANY_NAME', 'RoxHome')
IVA_PERCENT = float(os.getenv('IVA_PERCENT', '12'))
CURRENCY = 'USD'

for p in [DATA_DIR, EXPORT_DIR, BACKUP_DIR, UPLOADS_DIR, UPLOADS_DIR/'evidencias', UPLOADS_DIR/'documentos', UPLOADS_DIR/'firmas', UPLOADS_DIR/'campanas']:
    p.mkdir(parents=True, exist_ok=True)

ROLES = ['Administrador','Dirección','Coordinación','Ventas','Técnico','Marketing','Solo lectura']
LEAD_STATES = ['Nuevo','Contactado','Calificado','Visita agendada','Cotizado','Seguimiento','Ganado','Perdido']
LEAD_SOURCES = ['Facebook','Instagram','WhatsApp','Referido','Página web','Cliente antiguo','Campaña local','Otro']
SERVICES = ['Cámaras','Cerco eléctrico','Sensores','Redes','Computadoras','Mantenimiento','Domótica','Otro']
PRIORITIES = ['Baja','Media','Alta','Urgente']
DEAL_STAGES = ['Nuevo','Diagnóstico','Cotización','Negociación','Ganado','Perdido','Instalado','Cobrado']
SERVICE_STATES = ['Programado','En camino','En proceso','Pausado','Terminado','Requiere revisión','Cancelado']
INVOICE_STATES = ['Pendiente','Pagada','Parcial','Vencida','Anulada']
PAYMENT_METHODS = ['Efectivo','Transferencia','Tarjeta','Crédito','Otro']
PRODUCT_CATEGORIES = ['Cámara','NVR','DVR','Disco duro','Cable','Conector','Fuente','Sensor','Cerco eléctrico','Computadora','Repuesto','Servicio','Otro']
