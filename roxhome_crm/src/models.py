from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text, Time
from datetime import datetime, date
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Campaign(Base):
    __tablename__ = 'campanas'
    id = Column(Integer, primary_key=True)
    campana_codigo = Column(String, unique=True)
    nombre = Column(String, nullable=False)
    plataforma = Column(String)
    presupuesto = Column(Float, default=0)
    gasto_real = Column(Float, default=0)
    leads_generados = Column(Integer, default=0)
    ventas_generadas = Column(Float, default=0)
    estado = Column(String, default='Activa')

class Lead(Base):
    __tablename__ = 'posibles_clientes'
    id = Column(Integer, primary_key=True)
    lead_codigo = Column(String, unique=True)
    fecha_creacion = Column(Date, default=date.today)
    hora_creacion = Column(Time, default=lambda: datetime.now().time())
    nombre_cliente = Column(String, nullable=False)
    telefono = Column(String)
    whatsapp = Column(String)
    email = Column(String)
    ciudad = Column(String)
    direccion = Column(String)
    tipo_cliente = Column(String)
    fuente = Column(String)
    campana_id = Column(Integer, ForeignKey('campanas.id'))
    servicio_interes = Column(String)
    descripcion_necesidad = Column(Text)
    presupuesto_estimado = Column(Float, default=0)
    urgencia = Column(String, default='Media')
    estado = Column(String, default='Nuevo')
    responsable_id = Column(Integer, ForeignKey('users.id'))
    tiempo_respuesta_minutos = Column(Integer)
    motivo_perdida = Column(Text)
    observaciones = Column(Text)
    proximo_seguimiento = Column(Date)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Account(Base):
    __tablename__ = 'cuentas'
    id = Column(Integer, primary_key=True)
    cuenta_codigo = Column(String, unique=True)
    nombre_empresa = Column(String, nullable=False)
    tipo_cuenta = Column(String)
    ruc_cedula = Column(String)
    telefono = Column(String)
    email = Column(String)
    ciudad = Column(String)
    direccion = Column(String)
    estado = Column(String, default='Activa')
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Contact(Base):
    __tablename__ = 'contactos'
    id = Column(Integer, primary_key=True)
    contacto_codigo = Column(String, unique=True)
    lead_id = Column(Integer, ForeignKey('posibles_clientes.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'))
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Deal(Base):
    __tablename__ = 'tratos'
    id = Column(Integer, primary_key=True)
    trato_codigo = Column(String, unique=True)
    lead_id = Column(Integer, ForeignKey('posibles_clientes.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'))
    contacto_id = Column(Integer, ForeignKey('contactos.id'))
    nombre_trato = Column(String, nullable=False)
    servicio_principal = Column(String)
    etapa = Column(String, default='Nuevo')
    valor_estimado = Column(Float, default=0)
    probabilidad = Column(Float, default=0)
    fecha_cierre_estimada = Column(Date)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    producto_codigo = Column(String, unique=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String)
    costo = Column(Float, default=0)
    precio_venta = Column(Float, default=0)
    margen = Column(Float, default=0)
    stock_actual = Column(Float, default=0)
    stock_minimo = Column(Float, default=0)
    activo = Column(Boolean, default=True)

class Quote(Base):
    __tablename__ = 'presupuestos'
    id = Column(Integer, primary_key=True)
    presupuesto_codigo = Column(String, unique=True)
    lead_id = Column(Integer, ForeignKey('posibles_clientes.id'))
    deal_id = Column(Integer, ForeignKey('tratos.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'))
    fecha = Column(Date, default=date.today)
    valido_hasta = Column(Date)
    estado = Column(String, default='Borrador')
    subtotal = Column(Float, default=0)
    descuento = Column(Float, default=0)
    iva = Column(Float, default=0)
    total = Column(Float, default=0)
    notas = Column(Text)
    condiciones = Column(Text)

class QuoteItem(Base):
    __tablename__ = 'presupuesto_items'
    id = Column(Integer, primary_key=True)
    presupuesto_id = Column(Integer, ForeignKey('presupuestos.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=True)
    descripcion = Column(String)
    cantidad = Column(Float, default=1)
    costo_unitario = Column(Float, default=0)
    precio_unitario = Column(Float, default=0)
    descuento = Column(Float, default=0)
    subtotal = Column(Float, default=0)

class SalesOrder(Base):
    __tablename__ = 'ordenes_venta'
    id = Column(Integer, primary_key=True)
    orden_codigo = Column(String, unique=True)
    presupuesto_id = Column(Integer, ForeignKey('presupuestos.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'))
    fecha = Column(Date, default=date.today)
    estado = Column(String, default='Pendiente')
    total = Column(Float, default=0)

class Technician(Base):
    __tablename__ = 'tecnicos'
    id = Column(Integer, primary_key=True)
    tecnico_codigo = Column(String, unique=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    especialidad = Column(String)
    nivel = Column(String)
    activo = Column(Boolean, default=True)

class Service(Base):
    __tablename__ = 'servicios_tecnicos'
    id = Column(Integer, primary_key=True)
    servicio_codigo = Column(String, unique=True)
    orden_venta_id = Column(Integer, ForeignKey('ordenes_venta.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'))
    tipo_servicio = Column(String)
    descripcion = Column(Text)
    direccion = Column(String)
    ubicacion_google_maps = Column(String)
    materiales = Column(Text)
    fecha_programada = Column(Date)
    tecnico_lider_id = Column(Integer, ForeignKey('tecnicos.id'))
    tecnico_apoyo_id = Column(Integer, ForeignKey('tecnicos.id'))
    estado = Column(String, default='Programado')
    saldo_pendiente = Column(Float, default=0)
    observaciones_internas = Column(Text)
    falta_material = Column(Boolean, default=False)
    hubo_problema = Column(Boolean, default=False)

class ServiceChecklist(Base):
    __tablename__ = 'checklists'
    id = Column(Integer, primary_key=True)
    servicio_id = Column(Integer, ForeignKey('servicios_tecnicos.id'))
    item = Column(String)
    completado = Column(Boolean, default=False)

class ServiceEvidence(Base):
    __tablename__ = 'evidencias_servicio'
    id = Column(Integer, primary_key=True)
    servicio_id = Column(Integer, ForeignKey('servicios_tecnicos.id'))
    tipo = Column(String)
    ruta_archivo = Column(String)
    descripcion = Column(Text)
    fecha_subida = Column(DateTime, default=datetime.utcnow)

class Invoice(Base):
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True)
    factura_codigo = Column(String, unique=True)
    orden_venta_id = Column(Integer, ForeignKey('ordenes_venta.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'))
    fecha_emision = Column(Date, default=date.today)
    fecha_vencimiento = Column(Date)
    estado = Column(String, default='Pendiente')
    total = Column(Float, default=0)
    pagado = Column(Float, default=0)
    saldo = Column(Float, default=0)
