import streamlit as st
import pandas as pd
from datetime import date, timedelta
from ..models import Quote, QuoteItem, Product, Lead, Account
from ..crud import approve_quote
from ..utils import next_code
from ..config import IVA_PERCENT, COMPANY_NAME
from ..export_excel import export_quote_excel

try:
    from fpdf import FPDF
    PDF_OK = True
except Exception:
    PDF_OK = False

QUOTE_STATES = ['Borrador', 'Enviado', 'Aprobado', 'Rechazado', 'Vencido']


def _client_options(leads, accounts):
    return [('lead', l.id, l.nombre_cliente) for l in leads] + [('account', a.id, a.nombre_empresa) for a in accounts]


def _export_pdf(quote, items_df, client_name):
    from ..config import EXPORT_DIR
    pdf = FPDF(); pdf.add_page(); pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, COMPANY_NAME, ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f"Presupuesto: {quote.presupuesto_codigo} | Fecha: {quote.fecha}", ln=True)
    pdf.cell(0, 8, f"Cliente: {client_name}", ln=True)
    for _, r in items_df.iterrows():
        pdf.cell(0, 7, f"{r['descripcion']} | Cant {r['cantidad']} | ${r['subtotal']:.2f}", ln=True)
    pdf.cell(0, 8, f"Subtotal: ${quote.subtotal:.2f}  Desc: ${quote.descuento:.2f}  IVA: ${quote.iva:.2f}  Total: ${quote.total:.2f}", ln=True)
    pdf.cell(0, 8, f"Validez: {quote.valido_hasta}", ln=True)
    pdf.cell(0, 8, f"Condiciones: {quote.condiciones or ''}", ln=True)
    out = EXPORT_DIR / f"presupuesto_{quote.presupuesto_codigo}.pdf"
    pdf.output(str(out))
    return out


def render(db, user):
    st.title('Presupuestos profesionales')
    if 'quote_items' not in st.session_state:
        st.session_state.quote_items = []

    leads = db.query(Lead).all(); accounts = db.query(Account).all(); products = db.query(Product).all()
    client_options = _client_options(leads, accounts)

    st.subheader('Nuevo presupuesto')
    a, b, c = st.columns(3)
    selected = a.selectbox('Cliente', client_options, format_func=lambda x: f"{x[2]} ({x[0]})") if client_options else None
    valido = b.date_input('Validez', date.today() + timedelta(days=10))
    estado = c.selectbox('Estado', QUOTE_STATES)
    condiciones = st.text_area('Condiciones', 'Precios en USD. No incluye obras civiles.')
    notas = st.text_area('Observaciones')

    st.markdown('#### Agregar líneas')
    l1, l2, l3, l4 = st.columns([2, 2, 1, 1])
    line_type = l1.selectbox('Tipo', ['Producto inventario', 'Servicio manual', 'Mano de obra'])
    if line_type == 'Producto inventario' and products:
        prod = l2.selectbox('Producto', products, format_func=lambda x: f"{x.nombre} (${x.precio_venta})")
        desc, pid, cost, price = prod.nombre, prod.id, prod.costo or 0, prod.precio_venta or 0
    else:
        prod = None
        desc = l2.text_input('Descripción')
        pid = None
        cost = l3.number_input('Costo', min_value=0.0, value=0.0)
        price = l4.number_input('Precio', min_value=0.0, value=0.0)

    d1, d2, d3 = st.columns(3)
    qty = d1.number_input('Cantidad', min_value=1.0, value=1.0)
    dsc = d2.number_input('Descuento línea', min_value=0.0, value=0.0)
    if d3.button('Agregar línea'):
        if desc:
            st.session_state.quote_items.append({'producto_id': pid, 'descripcion': desc, 'cantidad': qty, 'costo_unitario': cost, 'precio_unitario': price, 'descuento': dsc, 'subtotal': qty*price-dsc})
            st.success('Línea agregada')

    items_df = pd.DataFrame(st.session_state.quote_items)
    if not items_df.empty:
        st.dataframe(items_df, use_container_width=True)

    discount = st.number_input('Descuento global', min_value=0.0, value=0.0)
    subtotal = float(items_df['subtotal'].sum()) if not items_df.empty else 0.0
    iva = (subtotal - discount) * (IVA_PERCENT / 100)
    total = subtotal - discount + iva
    margin = total - float((items_df['cantidad'] * items_df['costo_unitario']).sum()) if not items_df.empty else total
    m1, m2, m3, m4 = st.columns(4)
    m1.metric('Subtotal', f'${subtotal:,.2f}')
    m2.metric('IVA', f'${iva:,.2f}')
    m3.metric('Total', f'${total:,.2f}')
    m4.metric('Margen estimado', f'${margin:,.2f}')

    if st.button('Guardar presupuesto'):
        if selected is None or items_df.empty:
            st.error('Seleccione cliente y agregue líneas.')
        else:
            typ, cid, _ = selected
            q = Quote(presupuesto_codigo=next_code('PRE', db.query(Quote).count()), lead_id=cid if typ == 'lead' else None, cuenta_id=cid if typ == 'account' else None, fecha=date.today(), valido_hasta=valido, estado=estado, subtotal=subtotal, descuento=discount, iva=iva, total=total, condiciones=condiciones, notas=notas)
            db.add(q); db.flush()
            for _, it in items_df.iterrows():
                db.add(QuoteItem(presupuesto_id=q.id, producto_id=it['producto_id'], descripcion=it['descripcion'], cantidad=it['cantidad'], costo_unitario=it['costo_unitario'], precio_unitario=it['precio_unitario'], descuento=it['descuento'], subtotal=it['subtotal']))
            db.commit(); st.session_state.quote_items = []
            st.success(f'Presupuesto creado: {q.presupuesto_codigo}')

    st.divider(); st.subheader('Presupuestos registrados')
    qs = pd.read_sql(db.query(Quote).statement, db.bind)
    st.dataframe(qs, use_container_width=True)
    if not qs.empty:
        qid = int(st.selectbox('Seleccionar presupuesto', qs['id'].tolist()))
        quote = db.get(Quote, qid)
        items = pd.read_sql(db.query(QuoteItem).filter(QuoteItem.presupuesto_id == qid).statement, db.bind)
        client_name = 'Cliente'
        if quote.cuenta_id:
            acc = db.get(Account, quote.cuenta_id); client_name = acc.nombre_empresa if acc else 'Cuenta'
        elif quote.lead_id:
            ld = db.get(Lead, quote.lead_id); client_name = ld.nombre_cliente if ld else 'Lead'

        e1, e2, e3, e4 = st.columns(4)
        new_state = e1.selectbox('Estado', QUOTE_STATES, index=QUOTE_STATES.index(quote.estado) if quote.estado in QUOTE_STATES else 0)
        if e1.button('Actualizar estado'):
            quote.estado = new_state; db.commit(); st.success('Estado actualizado')
        if e2.button('Exportar Excel profesional'):
            path = export_quote_excel(quote, items, client_name); st.success(f'Excel: {path.name}')
        if e3.button('Exportar PDF'):
            if PDF_OK:
                p = _export_pdf(quote, items, client_name); st.success(f'PDF: {p.name}')
            else:
                st.warning('Instale fpdf2 para PDF: pip install fpdf2')
        if e4.button('Aprobar y crear orden'):
            order = approve_quote(db, qid)
            if order: st.success(f'Orden creada: {order.orden_codigo}')
