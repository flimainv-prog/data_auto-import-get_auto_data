import yfinance as yf
import pandas as pd
import numpy as np

def fetch_asset(symbols):
    """Tenta buscar dados de uma lista de símbolos até encontrar um válido."""
    for sym in symbols:
        try:
            # Tenta buscar os últimos 2 dias para ter o fechamento anterior
            df = yf.download(sym, period='2d', interval='1d', progress=False)
            if not df.empty and len(df) >= 1:
                latest = df.iloc[-1]
                price = float(latest['Close'])
                open_p = float(latest['Open'])
                
                # Cálculo de variação
                if len(df) > 1:
                    prev_close = float(df['Close'].iloc[-2])
                    change_pct = ((price - prev_close) / prev_close) * 100
                else:
                    change_pct = 0.0
                
                return {
                    'status': 'success',
                    'symbol_used': sym,
                    'price': price,
                    'open': open_p,
                    'change_pct': change_pct,
                    'source': 'Yahoo Finance'
                }
        except:
            continue
    
    return {
        'status': 'error',
        'symbol_used': symbols[0],
        'price': np.nan,
        'open': np.nan,
        'change_pct': np.nan,
        'source': 'N/A'
    }

def get_auto_data():
    """Função principal que o app.py vai chamar."""
    # Usando tickers estáveis (Spot e Futuros principais)
    return {
        'WDO': fetch_asset(['USDBRL=X', 'BRL=X']),
        'DXY': fetch_asset(['DX=F', 'DX-Y.NYB']),
        '6L': fetch_asset(['GBPUSD=X', '6L=F'])
    }
