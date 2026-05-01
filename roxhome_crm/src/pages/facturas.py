import streamlit as st
import pandas as pd
from datetime import date, timedelta
from ..models import Invoice, SalesOrder
from ..utils import next_code, invoice_status
from ..crud import update_invoice_payment

def render(db, user):
    st.title('Facturas')
    orders = db.query(SalesOrder).all()

    with st.form('new_invoice'):
        oid = st.selectbox('Orden de venta', [0] + [o.id for o in orders], format_func=lambda x: 'Seleccione orden' if x == 0 else f'Orden #{x}')
        total = st.number_input('Total', min_value=0.0, value=0.0)
        venc = st.date_input('Vence', date.today() + timedelta(days=15))
        submit = st.form_submit_button('Crear factura')
        if submit:
            if oid == 0:
                st.error('Debe seleccionar una orden de venta.')
            else:
                est, saldo = invoice_status(total, 0, venc)
                inv = Invoice(
                    factura_codigo=next_code('FAC', db.query(Invoice).count()),
                    orden_venta_id=oid,
                    total=total,
                    fecha_vencimiento=venc,
                    estado=est,
                    saldo=saldo,
                )
                db.add(inv)
                db.commit()
                st.success('Factura creada')

    df = pd.read_sql(db.query(Invoice).statement, db.bind)
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        iid = int(st.selectbox('Registrar pago', df['id'].tolist()))
        paid = st.number_input('Pagado', min_value=0.0, value=0.0)
        if st.button('Actualizar pago'):
            invoice = update_invoice_payment(db, iid, paid)
            if invoice:
                st.success(f'Factura actualizada. Estado: {invoice.estado} | Saldo: ${invoice.saldo:,.2f}')
            else:
                st.error('Factura no encontrada.')
