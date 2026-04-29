import streamlit as st
import pandas as pd
from data_auto import get_auto_data

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📈 Dashboard WDO / DXY / 6L")

def force_df(obj):
    if isinstance(obj, pd.DataFrame):
        return obj
    return pd.DataFrame()

try:
    data = get_auto_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

if not isinstance(data, dict):
    st.error("get_auto_data() não retornou dict")
    st.stop()

wdo = force_df(data.get("WDO"))
dxy = force_df(data.get("DXY"))
l6 = force_df(data.get("6L"))

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("WDO")
    if not wdo.empty:
        st.write(wdo.tail(1))
    else:
        st.warning("Sem dados")

with c2:
    st.subheader("DXY")
    if not dxy.empty:
        st.write(dxy.tail(1))
    else:
        st.warning("Sem dados")

with c3:
    st.subheader("6L")
    if not l6.empty:
        st.write(l6.tail(1))
    else:
        st.warning("Sem dados")
