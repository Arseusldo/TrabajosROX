import streamlit as st
import pandas as pd
import plotly.express as px
from ..models import Lead, Invoice, Product

def render(db, user):
    st.title('Informes')
    leads = pd.read_sql(db.query(Lead).statement, db.bind)
    if not leads.empty:
        st.plotly_chart(px.histogram(leads, x='estado', title='Leads por estado'), use_container_width=True)
    inv = pd.read_sql(db.query(Invoice).statement, db.bind)
    if not inv.empty:
        st.plotly_chart(px.pie(inv, names='estado', values='total', title='Facturas por estado'), use_container_width=True)
    prod = pd.read_sql(db.query(Product).statement, db.bind)
    if not prod.empty:
        st.dataframe(prod[prod['stock_actual']<=prod['stock_minimo']], use_container_width=True)
