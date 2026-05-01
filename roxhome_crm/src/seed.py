from .models import User, Technician, Product, Lead, Campaign
from .auth import hash_password

def seed(db):
    if not db.query(User).filter_by(email='admin@roxhome.local').first():
        db.add(User(nombre='Administrador RoxHome', email='admin@roxhome.local', password_hash=hash_password('admin123'), rol='Administrador'))
    if not db.query(User).filter_by(email='tecnico@roxhome.local').first():
        db.add(User(nombre='Carlos Vega', email='tecnico@roxhome.local', password_hash=hash_password('tecnico123'), rol='Técnico'))
    if db.query(Technician).count()==0:
        db.add_all([Technician(tecnico_codigo='TEC-0001', nombre='Carlos Vega', especialidad='Cámaras', nivel='Senior'), Technician(tecnico_codigo='TEC-0002', nombre='Ana Torres', especialidad='Redes', nivel='Medio')])
    if db.query(Product).count()==0:
        db.add_all([Product(producto_codigo='PRO-0001', nombre='Cámara IP 2MP', categoria='Cámara', costo=30, precio_venta=55, margen=25, stock_actual=25, stock_minimo=5), Product(producto_codigo='PRO-0002', nombre='Router WiFi 6', categoria='Otro', costo=45, precio_venta=75, margen=30, stock_actual=10, stock_minimo=3)])
    if db.query(Campaign).count()==0:
        db.add(Campaign(campana_codigo='CAM-0001', nombre='Leads Facebook Abril', plataforma='Facebook', presupuesto=200, gasto_real=150, leads_generados=12, estado='Activa'))
    if db.query(Lead).count()==0:
        db.add(Lead(lead_codigo='LEAD-0001', nombre_cliente='Comercial Andrade', telefono='0990000001', fuente='Facebook', servicio_interes='Cámaras', estado='Nuevo', urgencia='Alta'))
    db.commit()
