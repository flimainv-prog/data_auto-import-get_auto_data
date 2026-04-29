# data_auto.py

import yfinance as yf
import pandas as pd


def get_auto_data():
    """
    Busca dados para WDO, DXY e 6L (usando DOL como proxy robusto).
    Tenta múltiplos tickers candidatos, períodos e intervalos.
    Retorna dict com DataFrames ou None se falhar.
    """
    def fetch_df(candidates, periods=['5d', '1mo'], intervals=['1d', '1h']):
        for period in periods:
            for interval in intervals:
                for cand in candidates:
                    try:
                        ticker = yf.Ticker(cand)
                        hist = ticker.history(period=period, interval=interval, prepost=False)
                        if not hist.empty and len(hist) >= 2:
                            df = hist[['Open', 'High', 'Low', 'Close', 'Volume']].dropna(how='all').tail(10)
                            if not df.empty:
                                return df
                    except Exception:
                        continue
        return None

    # Candidatos atualizados para outubro/2024 e próximos
    wdo_candidates = ['WDOX24.SA', 'WDOV24.SA', 'WDOZ24.SA', 'WDOF25.SA', 'WDOG25.SA']
    dxy_candidates = ['DX-Y.NYB', 'DXY']
    sixl_candidates = ['DOLX24.SA', 'DOLV24.SA', 'DOLZ24.SA', 'DOLF25.SA']  # 6L como DOL (dólar futuro)

    data = {
        'WDO': fetch_df(wdo_candidates),
        'DXY': fetch_df(dxy_candidates),
        '6L': fetch_df(sixl_candidates)
    }

    return data


# app.py

import streamlit as st
import pandas as pd
import data_auto
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Auto",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Dashboard Automático - WDO, DXY e 6L")
st.markdown("*Dados atualizados automaticamente a cada 5 minutos (TTL cache).*")

@st.cache_data(ttl=300)  # 5 minutos de cache
@st.cache_data.show_data()
def load_data():
    return data_auto.get_auto_data()

data = load_data()

# Botão de atualização manual
col_btn, col_time = st.columns([3, 1])
with col_btn:
    if st.button("🔄 Atualizar Dados Agora", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
with col_time:
    st.caption(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Colunas para exibição
col1, col2, col3 = st.columns(3)

def display_asset_section(column, title, data_key):
    with column:
        st.subheader(f"{title}")
        df = data.get(data_key)
        if df is not None and not df.empty:
            # Tabela formatada
            styled_df = df.style.format({
                'Open': '{:.4f}',
                'High': '{:.4f}',
                'Low': '{:.4f}',
                'Close': '{:.4f}',
                'Volume': '{:.0f}'
            }).background_gradient(subset=['Close'], cmap='RdYlGn')
            st.dataframe(styled_df, height=300, use_container_width=True)
            
            # Métricas
            last_close = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            change = last_close - prev_close
            change_pct = (change / prev_close) * 100
            st.metric(
                label="Último Fechamento",
                value=f"{last_close:.4f}",
                delta=f"{change:+.4f} ({change_pct:+.2f}%)")
        else:
            st.warning(f"⚠️ Dados para **{title}** indisponíveis no momento.\nTente atualizar ou verifique conexão.")
            st.caption("Outros ativos continuam funcionando.")

# Exibe seções independentes
display_asset_section(col1, "🤝 WDO", "WDO")
display_asset_section(col2, "💵 DXY", "DXY")
display_asset_section(col3, "📊 6L", "6L")

st.markdown("---")
st.caption("Compatível com Streamlit 1.38.0, pandas 2.2.2, yfinance 0.2.40. Sem loops agressivos ou sleep.")
