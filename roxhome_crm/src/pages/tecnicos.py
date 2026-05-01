import streamlit as st
import pandas as pd
from ..models import Technician
from ..utils import next_code

def render(db, user):
    st.title('Técnicos')
    with st.form('new_tech'):
        nombre = st.text_input('Nombre')
        esp = st.selectbox('Especialidad', ['Cámaras','Cercos','Redes','Computadoras','General'])
        nivel = st.selectbox('Nivel', ['Junior','Medio','Senior','Líder'])
        if st.form_submit_button('Guardar') and nombre:
            db.add(Technician(tecnico_codigo=next_code('TEC', db.query(Technician).count()), nombre=nombre, especialidad=esp, nivel=nivel))
            db.commit(); st.success('Técnico creado')
    st.dataframe(pd.read_sql(db.query(Technician).statement, db.bind), use_container_width=True)
