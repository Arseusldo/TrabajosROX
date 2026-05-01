import streamlit as st
import pandas as pd
from ..models import Campaign
from ..utils import next_code

def render(db, user):
    st.title('Campañas')
    with st.form('new_campaign'):
        nombre = st.text_input('Nombre')
        plataforma = st.selectbox('Plataforma', ['Facebook','Instagram','TikTok','WhatsApp','Referidos','Local','Otro'])
        presupuesto = st.number_input('Presupuesto', 0.0)
        gasto = st.number_input('Gasto real', 0.0)
        leads = st.number_input('Leads generados', 0)
        if st.form_submit_button('Guardar') and nombre:
            db.add(Campaign(campana_codigo=next_code('CAM', db.query(Campaign).count()), nombre=nombre, plataforma=plataforma, presupuesto=presupuesto, gasto_real=gasto, leads_generados=leads))
            db.commit(); st.success('Campaña creada')
    st.dataframe(pd.read_sql(db.query(Campaign).statement, db.bind), use_container_width=True)
