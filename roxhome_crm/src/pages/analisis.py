import streamlit as st
from ..models import Lead, Deal, Quote, Invoice

def render(db, user):
    st.title('Análisis gerencial')
    leads = db.query(Lead).count()
    deals = db.query(Deal).count()
    quotes = db.query(Quote).count()
    approved = db.query(Quote).filter(Quote.estado=='Aprobado').count()
    inv = db.query(Invoice).all()
    total = sum(i.total for i in inv)
    pendiente = sum(i.saldo for i in inv)
    conversion = (deals/leads*100) if leads else 0
    appr = (approved/quotes*100) if quotes else 0
    st.metric('Tasa conversión lead->trato', f'{conversion:.1f}%')
    st.metric('Tasa cotización aprobada', f'{appr:.1f}%')
    st.metric('Total facturado', f'${total:,.2f}')
    st.metric('Total pendiente', f'${pendiente:,.2f}')
