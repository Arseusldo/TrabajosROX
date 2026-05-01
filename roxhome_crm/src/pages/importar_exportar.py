import streamlit as st
from ..export_excel import export_all
from ..backup import create_backup

def render(db, user):
    st.title('Importar / Exportar y Backups')
    if st.button('Exportar toda la base a Excel'):
        path = export_all(db.bind)
        st.success(f'Exportado: {path.name}')
    if st.button('Crear backup de SQLite'):
        path = create_backup()
        st.success(f'Backup creado: {path.name}')
