import streamlit as st

GROUPS = {
    'General': ['Inicio', 'Informes', 'Análisis', 'Mis solicitudes', 'Cola de trabajo'],
    'Ventas': ['Posibles clientes', 'Contactos', 'Cuentas', 'Tratos', 'Previsiones', 'Documentos', 'Campañas'],
    'Actividades': ['Tareas', 'Reuniones', 'Llamadas'],
    'Inventario': ['Productos', 'Catálogos de precios', 'Presupuestos', 'Órdenes de venta', 'Órdenes de compra', 'Facturas', 'Proveedores'],
    'Asistencia': ['Casos', 'Soluciones'],
    'Integraciones': ['SalesInbox', 'Social', 'Visitas'],
    'Servicios': ['Servicios técnicos', 'Instalaciones', 'Mantenimientos', 'Garantías', 'Técnicos', 'Horarios', 'Checklists', 'Evidencias'],
    'Projects': ['Proyectos'],
    'Sistema': ['Configuración', 'Importar/Exportar Excel'],
}

def render_sidebar(user_name:str, role:str):
    st.sidebar.markdown(f"### {user_name}")
    st.sidebar.caption(role)
    all_pages = []
    labels = []
    for group, pages in GROUPS.items():
        labels.append(f"— {group} —")
        all_pages.extend([(group, p) for p in pages])
    st.sidebar.markdown('---')
    group = st.sidebar.selectbox('Grupo', list(GROUPS.keys()))
    page = st.sidebar.radio('Módulos', GROUPS[group], label_visibility='collapsed')
    logout = st.sidebar.button('Cerrar sesión')
    return page, logout
