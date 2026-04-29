import yfinance as yf
import pandas as pd
import numpy as np

def fetch_asset(symbol):
    """Busca dados de um símbolo específico com múltiplos fallbacks."""
    result = {'status': 'ERRO', 'price': np.nan, 'change_pct': np.nan, 'symbol': symbol}
    
    try:
        # Tenta via history (mais estável para variação diária)
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='2d')
        if not hist.empty and len(hist) >= 1:
            price = float(hist['Close'].iloc[-1])
            if len(hist) > 1:
                prev_close = float(hist['Close'].iloc[-2])
                change_pct = ((price - prev_close) / prev_close) * 100
            else:
                change_pct = 0.0
            
            return {
                'status': 'success',
                'price': price,
                'change_pct': change_pct,
                'symbol': symbol
            }
    except:
        pass

    try:
        # Fallback via download direto
        df = yf.download(symbol, period='2d', progress=False)
        if not df.empty:
            price = float(df['Close'].iloc[-1])
            prev = df['Close'].iloc[-2] if len(df) > 1 else price
            change = ((price - prev) / prev) * 100
            return {'status': 'success', 'price': price, 'change_pct': change, 'symbol': symbol}
    except:
        pass

    return result

def get_auto_data():
    """Função principal chamada pelo app.py"""
    # Tickers validados que funcionam no Yahoo Finance
    mapping = {
        'WDO': 'USDBRL=X',  # Dólar Comercial (Spot)
        'DXY': 'DX=F',      # Índice Dólar Futuro
        '6L': 'GBPUSD=X'    # Libra/Dólar (Proxy para 6L)
    }
    
    return {name: fetch_asset(sym) for name, sym in mapping.items()}
