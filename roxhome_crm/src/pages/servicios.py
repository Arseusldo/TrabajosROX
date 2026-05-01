import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
from ..models import Service, ServiceChecklist, ServiceEvidence, Technician
from ..config import UPLOADS_DIR

STATES_TECH = ['En camino', 'En proceso', 'Terminado', 'Requiere revisión']
STATES_ADMIN = ['Programado', 'En camino', 'En proceso', 'Pausado', 'Terminado', 'Requiere revisión', 'Cancelado']


def _save_file(uploaded_file, service_code, tipo):
    folder = UPLOADS_DIR / 'evidencias' / service_code
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{tipo}_{uploaded_file.name}"
    with open(path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return str(path)


def render(db, user):
    st.title('Servicios técnicos')
    techs = db.query(Technician).all()
    tech_map = {t.nombre: t.id for t in techs}

    q = db.query(Service)
    if user.rol == 'Técnico':
        my_tid = tech_map.get(user.nombre)
        if not my_tid:
            st.warning('No existe técnico asociado a este usuario. Solicite asignación al administrador.')
            return
        q = q.filter((Service.tecnico_lider_id == my_tid) | (Service.tecnico_apoyo_id == my_tid))

    services_df = pd.read_sql(q.statement, db.bind)
    if services_df.empty:
        st.info('No hay servicios para mostrar.')
        return

    if user.rol != 'Técnico':
        st.subheader('Vista administrador / coordinación')
        atrasados = services_df[(services_df['fecha_programada'].notna()) & (services_df['fecha_programada'] < pd.Timestamp(date.today())) & (services_df['estado'] != 'Terminado')]
        c1, c2, c3 = st.columns(3)
        c1.metric('Servicios totales', len(services_df))
        c2.metric('Atrasados', len(atrasados))
        c3.metric('Terminados', int((services_df['estado'] == 'Terminado').sum()))
        st.dataframe(services_df, use_container_width=True)

        prod = services_df.groupby('tecnico_lider_id').size().reset_index(name='trabajos')
        st.markdown('#### Productividad por técnico')
        st.dataframe(prod, use_container_width=True)
    else:
        st.subheader('Mis servicios asignados')
        show_cols = [c for c in ['id', 'servicio_codigo', 'tipo_servicio', 'direccion', 'ubicacion_google_maps', 'materiales', 'estado', 'fecha_programada'] if c in services_df.columns]
        st.dataframe(services_df[show_cols], use_container_width=True)

    sid = int(st.selectbox('Seleccionar servicio', services_df['id'].tolist()))
    service = db.get(Service, sid)

    st.markdown(f"### {service.servicio_codigo}")
    st.write(f"**Dirección:** {service.direccion or '-'}")
    st.write(f"**Ubicación:** {service.ubicacion_google_maps or '-'}")
    st.write(f"**Materiales:** {service.materiales or '-'}")

    checks = db.query(ServiceChecklist).filter_by(servicio_id=sid).all()
    st.markdown('#### Checklist')
    for c in checks:
        c.completado = st.checkbox(c.item, value=c.completado, key=f'chk_{c.id}')

    col1, col2 = st.columns(2)
    estado_options = STATES_TECH if user.rol == 'Técnico' else STATES_ADMIN
    service.estado = col1.selectbox('Estado', estado_options, index=estado_options.index(service.estado) if service.estado in estado_options else 0)
    service.falta_material = col1.checkbox('Falta material', value=bool(service.falta_material))
    service.hubo_problema = col2.checkbox('Hubo problema', value=bool(service.hubo_problema))
    service.observaciones_internas = col2.text_area('Observaciones', value=service.observaciones_internas or '')

    st.markdown('#### Evidencias (Antes/Después)')
    e1, e2 = st.columns(2)
    before_file = e1.file_uploader('Foto antes', type=['jpg', 'jpeg', 'png'], key='before')
    after_file = e2.file_uploader('Foto después', type=['jpg', 'jpeg', 'png'], key='after')

    if st.button('Guardar avance / checklist'):
        db.commit()
        if before_file:
            p = _save_file(before_file, service.servicio_codigo, 'antes')
            db.add(ServiceEvidence(servicio_id=sid, tipo='Antes', ruta_archivo=p, descripcion='Foto antes'))
        if after_file:
            p = _save_file(after_file, service.servicio_codigo, 'despues')
            db.add(ServiceEvidence(servicio_id=sid, tipo='Después', ruta_archivo=p, descripcion='Foto después'))
        db.commit()
        st.success('Actualización guardada')

    evidences = pd.read_sql(db.query(ServiceEvidence).filter_by(servicio_id=sid).statement, db.bind)
    if not evidences.empty:
        st.markdown('#### Fotos / evidencias cargadas')
        st.dataframe(evidences[['tipo', 'ruta_archivo', 'fecha_subida']], use_container_width=True)

    if user.rol != 'Técnico':
        st.markdown('#### Acciones administrativas')
        r1, r2 = st.columns(2)
        if techs:
            new_tid = r1.selectbox('Reasignar técnico líder', [t.id for t in techs], format_func=lambda tid: next((t.nombre for t in techs if t.id == tid), str(tid)))
            if r1.button('Guardar reasignación'):
                service.tecnico_lider_id = new_tid
                db.commit()
                st.success('Técnico reasignado')
        if r2.button('Generar garantía (marcar observación)'):
            service.observaciones_internas = (service.observaciones_internas or '') + '\n[Generar garantía sugerida]'
            db.commit(); st.success('Sugerencia de garantía registrada')
        if r2.button('Generar mantenimiento (marcar observación)'):
            service.observaciones_internas = (service.observaciones_internas or '') + '\n[Generar mantenimiento sugerido]'
            db.commit(); st.success('Sugerencia de mantenimiento registrada')
        if service.hubo_problema and r2.button('Crear caso por reclamo (marcar observación)'):
            service.observaciones_internas = (service.observaciones_internas or '') + '\n[Crear caso por reclamo]'
            db.commit(); st.success('Caso sugerido en observaciones')
