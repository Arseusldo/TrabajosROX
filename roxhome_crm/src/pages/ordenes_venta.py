import streamlit as st
import pandas as pd
from ..models import SalesOrder, Technician
from ..crud import create_service

def render(db, user):
    st.title('Órdenes de venta')
    orders_df = pd.read_sql(db.query(SalesOrder).statement, db.bind)
    st.dataframe(orders_df, use_container_width=True)

    techs = db.query(Technician).all()
    if orders_df.empty:
        st.info('No hay órdenes de venta.')
        return
    if not techs:
        st.warning('No hay técnicos registrados.')
        return

    oid = int(st.selectbox('Orden', orders_df['id'].tolist()))
    tid = int(st.selectbox('Técnico líder', [t.id for t in techs]))
    tipo = st.selectbox('Tipo servicio', ['Instalación cámaras', 'Cerco eléctrico', 'Redes'])
    if st.button('Crear servicio técnico'):
        service = create_service(db, dict(orden_venta_id=oid, tipo_servicio=tipo, tecnico_lider_id=tid))
        st.success(f'Servicio creado: {service.servicio_codigo}')
