import streamlit as st
from src.database import engine, SessionLocal, Base
from src.seed import seed
from src.auth import authenticate
from src.permissions import can_access
from src.ui.styles import inject_global_styles
from src.ui.sidebar import render_sidebar
from src.pages import inicio, informes, analisis, posibles_clientes, contactos, cuentas, tratos, previsiones, documentos, campanas, tareas, reuniones, llamadas, productos, catalogos_precios, presupuestos, ordenes_venta, ordenes_compra, facturas, proveedores, casos, soluciones, salesinbox, social, visitas, servicios, instalaciones, mantenimientos, garantias, tecnicos, horarios, checklists, evidencias, proyectos, configuracion, importar_exportar, mis_solicitudes, cola_trabajo

PAGES = {
'Inicio': inicio,'Informes': informes,'Análisis': analisis,'Mis solicitudes': mis_solicitudes,'Cola de trabajo': cola_trabajo,
'Posibles clientes': posibles_clientes,'Contactos': contactos,'Cuentas': cuentas,'Tratos': tratos,'Previsiones': previsiones,'Documentos': documentos,'Campañas': campanas,
'Tareas': tareas,'Reuniones': reuniones,'Llamadas': llamadas,
'Productos': productos,'Catálogos de precios': catalogos_precios,'Presupuestos': presupuestos,'Órdenes de venta': ordenes_venta,'Órdenes de compra': ordenes_compra,'Facturas': facturas,'Proveedores': proveedores,
'Casos': casos,'Soluciones': soluciones,'SalesInbox': salesinbox,'Social': social,'Visitas': visitas,
'Servicios técnicos': servicios,'Instalaciones': instalaciones,'Mantenimientos': mantenimientos,'Garantías': garantias,'Técnicos': tecnicos,'Horarios': horarios,'Checklists': checklists,'Evidencias': evidencias,
'Proyectos': proyectos,'Configuración': configuracion,'Importar/Exportar Excel': importar_exportar
}

def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal(); seed(db); db.close()

def login_view():
    st.markdown("<div class='rh-card'>", unsafe_allow_html=True)
    st.title('RoxHome CRM')
    c1, c2 = st.columns(2)
    email = c1.text_input('Email')
    password = c2.text_input('Contraseña', type='password')
    if st.button('Ingresar'):
        db = SessionLocal(); user = authenticate(db, email, password); db.close()
        if user:
            st.session_state.user = {'id': user.id, 'nombre': user.nombre, 'rol': user.rol}
            st.rerun()
        st.error('Credenciales inválidas')
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title='RoxHome CRM', layout='wide')
    inject_global_styles()
    init()
    if 'user' not in st.session_state:
        return login_view()

    page, logout = render_sidebar(st.session_state.user['nombre'], st.session_state.user['rol'])
    if logout:
        del st.session_state.user; st.rerun()

    if not can_access(st.session_state.user['rol'], page):
        st.error('No tienes permisos para este módulo.'); return
    db = SessionLocal()
    try:
        PAGES[page].render(db, type('U', (), st.session_state.user))
    finally:
        db.close()

if __name__ == '__main__':
    main()
