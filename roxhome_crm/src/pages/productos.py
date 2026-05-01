import streamlit as st
import pandas as pd
from ..models import Product
from ..utils import next_code

def render(db, user):
    st.title('Productos')
    with st.form('new_product'):
        nombre = st.text_input('Nombre*')
        costo = st.number_input('Costo', 0.0)
        precio = st.number_input('Precio venta', 0.0)
        stock = st.number_input('Stock', 0.0)
        min_stock = st.number_input('Stock mínimo', 0.0)
        if st.form_submit_button('Guardar') and nombre:
            p = Product(producto_codigo=next_code('PRO', db.query(Product).count()), nombre=nombre, costo=costo, precio_venta=precio, margen=precio-costo, stock_actual=stock, stock_minimo=min_stock)
            db.add(p); db.commit(); st.success('Producto guardado')
    df = pd.read_sql(db.query(Product).statement, db.bind)
    st.dataframe(df, use_container_width=True)
