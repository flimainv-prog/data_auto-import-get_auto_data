# data_auto.py

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Optional


def get_ticker_data(ticker: str) -> Optional[Dict]:
    """Helper para buscar dados intraday, tentando múltiplos intervalos."""
    intervals = ['1m', '2m', '5m', '15m', '30m', '60m']
    for interval in intervals:
        try:
            df = yf.download(ticker, period='1d', interval=interval, progress=False, group_by='ticker')
            if len(df) > 0:
                last = df.iloc[-1]
                open_price = last['Open']
                price = last['Close']
                change_abs = price - open_price
                change_pct = (change_abs / open_price * 100) if open_price != 0 else np.nan
                return {
                    'price': price,
                    'change_abs': change_abs,
                    'change_pct': change_pct
                }
        except Exception:
            continue
    return None


def get_market_data() -> Dict:
    """Busca dados de WDO, DXY e 6L com tratamento de erros robusto."""
    data = {}

    # WDO (ajuste o ticker para o contrato atual, ex: WDOZ24 para out/24)
    wdo_ticker = 'WDOZ24'
    wdo_raw = get_ticker_data(wdo_ticker)
    if wdo_raw:
        data.update({
            'wdo_price': wdo_raw['price'],
            'wdo_change_abs': wdo_raw['change_abs'],
            'wdo_change_pct': wdo_raw['change_pct'],
            'wdo_status': 'OK'
        })
    else:
        data.update({
            'wdo_price': np.nan,
            'wdo_change_abs': np.nan,
            'wdo_change_pct': np.nan,
            'wdo_status': 'Indisponível'
        })

    # DXY
    dxy_ticker = 'DX-Y.NYB'
    dxy_raw = get_ticker_data(dxy_ticker)
    if dxy_raw:
        data.update({
            'dxy_price': dxy_raw['price'],
            'dxy_change_abs': dxy_raw['change_abs'],
            'dxy_change_pct': dxy_raw['change_pct'],
            'dxy_status': 'OK'
        })
    else:
        data.update({
            'dxy_price': np.nan,
            'dxy_change_abs': np.nan,
            'dxy_change_pct': np.nan,
            'dxy_status': 'Indisponível'
        })

    # 6L (usa o mesmo helper robusto)
    sixl_ticker = '6L=F'
    sixl_raw = get_ticker_data(sixl_ticker)
    if sixl_raw:
        data.update({
            '6l_price': sixl_raw['price'],
            '6l_change_abs': sixl_raw['change_abs'],
            '6l_change_pct': sixl_raw['change_pct'],
            '6l_status': 'OK'
        })
    else:
        data.update({
            '6l_price': np.nan,
            '6l_change_abs': np.nan,
            '6l_change_pct': np.nan,
            '6l_status': 'Indisponível'
        })

    return data


# app.py

import streamlit as st
import pandas as pd
import numpy as np
from data_auto import get_market_data


st.set_page_config(
    page_title="Monitor de Mercado",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Monitor de Mercado - WDO, DXY e 6L")

# Botão de refresh manual (evita loops agressivos)
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    if st.button("🔄 Atualizar Dados", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

# Dados com cache leve (auto-refresh a cada 30s)
@st.cache_data(ttl=30)
def cached_get_market_data():
    return get_market_data()

data = cached_get_market_data()

# Verifica status do 6L e exibe aviso amigável
if data.get('6l_status') == 'Indisponível':
    st.warning("⚠️ O ticker 6L=F está indisponível no momento (sem dados intraday). Os dados de WDO e DXY continuam sendo exibidos normalmente.")

# Cria DataFrame para tabela
ativos = ['WDO', 'DXY', '6L']
df_data = {
    'Ativo': ativos,
    'Preço Atual': [
        data.get('wdo_price'),
        data.get('dxy_price'),
        data.get('6l_price')
    ],
    'Variação Abs': [
        data.get('wdo_change_abs'),
        data.get('dxy_change_abs'),
        data.get('6l_change_abs')
    ],
    'Variação %': [
        data.get('wdo_change_pct'),
        data.get('dxy_change_pct'),
        data.get('6l_change_pct')
    ],
    'Status': [
        data.get('wdo_status', 'Erro'),
        data.get('dxy_status', 'Erro'),
        data.get('6l_status', 'Erro')
    ]
}
df = pd.DataFrame(df_data)

# Função para colorir variações
def highlight_change(val):
    if pd.isna(val):
        return ''
    try:
        v = float(val)
        if v > 0:
            return 'background-color: #d4edda; color: #155724'
        elif v < 0:
            return 'background-color: #f8d7da; color: #721c24'
        else:
            return ''
    except:
        return ''

# Styler para formatação e cores
styler = df.style.format({
    'Preço Atual': '{:.4f}',
    'Variação Abs': '{:.4f}',
    'Variação %': '{:.2f}%'
}).map(highlight_change, subset=['Variação Abs', 'Variação %'])

# Exibe tabela
st.subheader("📊 Tabela de Dados")
st.dataframe(styler, use_container_width=True, hide_index=True)

# Métricas rápidas
st.subheader("📍 Métricas Rápidas")
col1, col2, col3 = st.columns(3)

with col1:
    wdo_p = data.get('wdo_price')
    wdo_pc = data.get('wdo_change_pct')
    if pd.isna(wdo_p):
        st.metric("WDO", "Indisponível")
    else:
        st.metric("WDO", f"{wdo_p:.4f}", f"{wdo_pc:+.2f}%")

with col2:
    dxy_p = data.get('dxy_price')
    dxy_pc = data.get('dxy_change_pct')
    if pd.isna(dxy_p):
        st.metric("DXY", "Indisponível")
    else:
        st.metric("DXY", f"{dxy_p:.4f}", f"{dxy_pc:+.2f}%")

with col3:
    sixl_p = data.get('6l_price')
    sixl_pc = data.get('6l_change_pct')
    if data.get('6l_status') != 'OK':
        st.metric("6L", "Indisponível")
    else:
        st.metric("6L", f"{sixl_p:.4f}", f"{sixl_pc:+.2f}%")
