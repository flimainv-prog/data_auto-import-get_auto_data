# ARQUIVO 2: app.py
import streamlit as st
import time
import pandas as pd
from data_auto import get_auto_data

st.set_page_config(page_title="Dados Auto", layout="wide")
st.title("📊 Dados WDO, 6L e DXY")

placeholder = st.empty()

try:
    data = get_auto_data()
    df = pd.DataFrame(list(data.items()), columns=["Métrica", "Valor"])
    placeholder.dataframe(df, use_container_width=True)
except Exception as e:
    placeholder.error(f"Erro ao carregar: {str(e)}")

time.sleep(10)
st.rerun()
