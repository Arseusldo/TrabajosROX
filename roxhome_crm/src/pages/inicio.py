import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from ..models import Lead, SalesOrder, Invoice, Service

def kpi_card(title, value):
    st.markdown(f"<div class='rh-card'><div class='rh-kpi-title'>{title}</div><div class='rh-kpi-value'>{value}</div></div>", unsafe_allow_html=True)

def render(db, user):
    st.title('Dashboard RoxHome')
    leads_total = db.query(Lead).count()
    ventas_total = db.query(SalesOrder).count()
    invoices = db.query(Invoice).all()
    cobrado = sum(i.pagado or 0 for i in invoices)
    pendiente = sum(i.saldo or 0 for i in invoices)
    servicios_hoy = db.query(Service).filter(Service.fecha_programada == date.today()).count()

    cols = st.columns(5)
    with cols[0]: kpi_card('Leads', leads_total)
    with cols[1]: kpi_card('Ventas', ventas_total)
    with cols[2]: kpi_card('Cobrado', f'${cobrado:,.2f}')
    with cols[3]: kpi_card('Saldo pendiente', f'${pendiente:,.2f}')
    with cols[4]: kpi_card('Servicios hoy', servicios_hoy)

    c1, c2 = st.columns(2)
    leads = pd.read_sql(db.query(Lead).statement, db.bind)
    if not leads.empty and 'fuente' in leads.columns:
        c1.markdown("<div class='rh-card'>", unsafe_allow_html=True)
        c1.plotly_chart(px.pie(leads, names='fuente', title='Leads por fuente'), use_container_width=True)
        c1.markdown("</div>", unsafe_allow_html=True)
    if not leads.empty and 'estado' in leads.columns:
        c2.markdown("<div class='rh-card'>", unsafe_allow_html=True)
        c2.plotly_chart(px.histogram(leads, x='estado', title='Leads por estado'), use_container_width=True)
        c2.markdown("</div>", unsafe_allow_html=True)

    services = pd.read_sql(db.query(Service).statement, db.bind)
    if not services.empty:
        st.markdown("#### Servicios recientes")
        st.dataframe(services.sort_values('id', ascending=False).head(10), use_container_width=True)
