import streamlit as st
import pandas as pd
from ..models import Lead
from ..crud import create_lead, convert_lead
from ..config import LEAD_STATES, LEAD_SOURCES, SERVICES, PRIORITIES

def render(db, user):
    st.title('Posibles clientes')
    with st.expander('Nuevo lead', expanded=False):
        with st.form('new_lead'):
            nombre = st.text_input('Nombre cliente*')
            tel = st.text_input('Teléfono')
            fuente = st.selectbox('Fuente', LEAD_SOURCES)
            servicio = st.selectbox('Servicio interés', SERVICES)
            estado = st.selectbox('Estado', LEAD_STATES)
            urg = st.selectbox('Urgencia', PRIORITIES)
            submit = st.form_submit_button('Guardar')
            if submit and nombre:
                create_lead(db, dict(nombre_cliente=nombre, telefono=tel, fuente=fuente, servicio_interes=servicio, estado=estado, urgencia=urg))
                st.success('Lead creado')
    leads = pd.read_sql(db.query(Lead).statement, db.bind)
    st.dataframe(leads, use_container_width=True)
    if not leads.empty:
        lead_id = st.selectbox('Convertir lead', leads['id'])
        if st.button('Convertir a contacto/cuenta/trato'):
            convert_lead(db, int(lead_id)); st.success('Lead convertido')
