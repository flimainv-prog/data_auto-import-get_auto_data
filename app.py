import streamlit as st
import pandas as pd
from data_auto import get_auto_data

st.set_page_config(
    page_title="Dashboard Auto Data",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Dashboard WDO, DXY e 6L")

# -----------------------------
# FUNÇÃO SEGURA
# -----------------------------
def safe_df(data, key):
    value = data.get(key)

    if isinstance(value, pd.DataFrame):
        return value

    if isinstance(value, dict):
        try:
            return pd.DataFrame(value)
        except:
            return pd.DataFrame()

    return pd.DataFrame()


# Botão atualização
col_btn_left, col_btn_right = st.columns([4, 1])

with col_btn_right:
    if st.button("🔄 Atualizar Dados", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("Última atualização: cache TTL = 30s")

# -----------------------------
# CARREGA DADOS
# -----------------------------
data = get_auto_data()

# Normaliza tudo para DataFrame
wdo = safe_df(data, "WDO")
dxy = safe_df(data, "DXY")
l6  = safe_df(data, "6L")

# -----------------------------
# CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇧🇷 WDO")

    if not wdo.empty:
        latest = wdo.iloc[-1]
        st.metric("Close", f"{latest['Close']:.4f}")
        st.caption(f"Volume: {latest['Volume']:.0f}")
    else:
        st.error("❌ Sem dados")

with col2:
    st.subheader("💵 DXY")

    if not dxy.empty:
        latest = dxy.iloc[-1]
        st.metric("Close", f"{latest['Close']:.2f}")
        st.caption(f"Volume: {latest['Volume']:.0f}")
    else:
        st.error("❌ Sem dados")

with col3:
    st.subheader("🔸 6L")

    if not l6.empty:
        latest = l6.iloc[-1]
        st.metric("Close", f"{latest['Close']:.4f}")
        st.caption(f"Volume: {latest['Volume']:.0f}")
    else:
        status = data.get("6L_status", "Indisponível")
        st.warning(f"⚠️ {status}")

# -----------------------------
# GRÁFICOS
# -----------------------------
if st.checkbox("Mostrar gráficos recentes"):
    st.markdown("---")

    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        if not wdo.empty:
            st.line_chart(wdo["Close"])

    with col_g2:
        if not dxy.empty:
            st.line_chart(dxy["Close"])

    with col_g3:
        if not l6.empty:
            st.line_chart(l6["Close"])

st.markdown("---")
st.caption("Fonte: Yahoo Finance | App blindado contra erros de dict/DataFrame")
