from sqlalchemy.orm import Session
from . import models
from .utils import next_code, invoice_status, CHECKLISTS


def create_lead(db: Session, data: dict):
    code = next_code('LEAD', db.query(models.Lead).count())
    lead = models.Lead(lead_codigo=code, **data)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def convert_lead(db: Session, lead_id: int):
    lead = db.get(models.Lead, lead_id)
    if not lead:
        return None

    account = models.Account(
        cuenta_codigo=next_code('CTA', db.query(models.Account).count()),
        nombre_empresa=lead.nombre_cliente,
        telefono=lead.telefono,
        email=lead.email,
        ciudad=lead.ciudad,
        direccion=lead.direccion,
        tipo_cuenta=lead.tipo_cliente or 'Hogar',
    )
    db.add(account)
    db.flush()

    contact = models.Contact(
        contacto_codigo=next_code('CON', db.query(models.Contact).count()),
        lead_id=lead.id,
        cuenta_id=account.id,
        nombre=lead.nombre_cliente,
        telefono=lead.telefono,
        email=lead.email,
    )
    db.add(contact)
    db.flush()

    deal = models.Deal(
        trato_codigo=next_code('TRA', db.query(models.Deal).count()),
        lead_id=lead.id,
        cuenta_id=account.id,
        contacto_id=contact.id,
        nombre_trato=f"Trato {lead.nombre_cliente}",
        servicio_principal=lead.servicio_interes,
        valor_estimado=lead.presupuesto_estimado or 0,
    )
    lead.estado = 'Ganado'
    db.add(deal)
    db.commit()
    return account, contact, deal


def approve_quote(db: Session, quote_id: int):
    q = db.get(models.Quote, quote_id)
    if not q:
        return None
    q.estado = 'Aprobado'
    order = models.SalesOrder(
        orden_codigo=next_code('OV', db.query(models.SalesOrder).count()),
        presupuesto_id=q.id,
        cuenta_id=q.cuenta_id,
        total=q.total or 0,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def create_service(db: Session, data: dict):
    order_id = data.get('orden_venta_id')
    if order_id:
        order = db.get(models.SalesOrder, order_id)
        if order and not data.get('cuenta_id'):
            data['cuenta_id'] = order.cuenta_id
    s = models.Service(servicio_codigo=next_code('SER', db.query(models.Service).count()), **data)
    db.add(s)
    db.flush()
    for item in CHECKLISTS.get(s.tipo_servicio, []):
        db.add(models.ServiceChecklist(servicio_id=s.id, item=item))
    db.commit()
    db.refresh(s)
    return s


def update_invoice_payment(db: Session, invoice_id: int, paid: float):
    inv = db.get(models.Invoice, invoice_id)
    if not inv:
        return None
    inv.pagado = max(paid, 0)
    inv.estado, inv.saldo = invoice_status(inv.total or 0, inv.pagado, inv.fecha_vencimiento)
    db.commit()
    db.refresh(inv)
    return inv
