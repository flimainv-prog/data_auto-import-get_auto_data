import streamlit as st
import yfinance as yf
import pandas as pd
from typing import Dict

@st.cache_data(ttl=30)
def get_auto_data() -> Dict[str, pd.DataFrame]:
    data: Dict[str, pd.DataFrame] = {}

    def safe_download(tickers: list, periods_intervals: list) -> pd.DataFrame:
        for ticker in tickers:
            for period, interval in periods_intervals:
                try:
                    df = yf.download(ticker, period=period, interval=interval, progress=False)
                    if not df.empty:
                        return df
                except Exception:
                    pass
        return pd.DataFrame()

    # WDO - Mini Dólar Futuro com fallbacks
    wdo_tickers = ['WDOU24.SA', 'WDOV24.SA', 'WDOZ24.SA', 'USDBRL=X']
    wdo_configs = [('2d', '5m'), ('5d', '15m')]
    wdo_df = safe_download(wdo_tickers, wdo_configs)
    data['WDO'] = wdo_df.tail(1) if not wdo_df.empty else pd.DataFrame()

    # DXY - US Dollar Index com fallbacks
    dxy_tickers = ['DX-Y.NYB', 'DX=F']
    dxy_configs = [('2d', '5m'), ('5d', '15m')]
    dxy_df = safe_download(dxy_tickers, dxy_configs)
    data['DXY'] = dxy_df.tail(1) if not dxy_df.empty else pd.DataFrame()

    # 6L com fallbacks (ajuste tickers se necessário)
    sixl_tickers = ['6L=F', 'SI=F']  # Exemplos; ajuste conforme necessário
    sixl_configs = [('1d', '1m'), ('2d', '5m')]
    sixl_df = safe_download(sixl_tickers, sixl_configs)
    if not sixl_df.empty:
        data['6L'] = sixl_df.tail(1)
    else:
        data['6L_status'] = 'Indisponível - sem dados nos tickers/intervalos testados'

    return data
