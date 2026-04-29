import yfinance as yf
import pandas as pd
import numpy as np


def get_auto_data():
    assets_config = {
        'WDO': ['WDOV24.SA', 'WDOU24.SA', 'WDOT24.SA'],
        'DXY': ['DX=F', 'DX-Y.NYB'],
        '6L': ['DOLV24.SA', 'DOLU24.SA', 'DOLT24.SA']
    }
    result = {}
    for asset, symbols in assets_config.items():
        found = False
        # Prioridade 1: ticker.info
        for sym in symbols:
            try:
                ticker = yf.Ticker(sym)
                info_dict = ticker.info
                price = (info_dict.get('regularMarketPrice') or 
                         info_dict.get('currentPrice') or 
                         info_dict.get('bid') or 
                         info_dict.get('ask'))
                if price is None or price == 0:
                    continue
                open_p = info_dict.get('regularMarketOpen') or info_dict.get('open')
                prev_close = info_dict.get('regularMarketPreviousClose') or info_dict.get('previousClose')
                change_abs = (info_dict.get('regularMarketChange') or 
                              (price - prev_close if prev_close else np.nan))
                change_pct = (info_dict.get('regularMarketChangePercent') or 
                              (change_abs / prev_close * 100 if prev_close and not pd.isna(change_abs) else np.nan))
                result[asset] = {
                    'symbol_used': sym,
                    'status': 'available',
                    'price': float(price),
                    'open': float(open_p) if open_p else np.nan,
                    'previous_close': float(prev_close) if prev_close else np.nan,
                    'change_abs': float(change_abs) if not pd.isna(change_abs) else np.nan,
                    'change_pct': float(change_pct) if not pd.isna(change_pct) else np.nan,
                    'source': 'ticker.info'
                }
                found = True
                break
            except Exception:
                continue
        if not found:
            # Fallback: history
            for sym in symbols:
                try:
                    hist = yf.download(sym, period='2d', progress=False)
                    if not hist.empty and len(hist) >= 1:
                        price = float(hist['Close'].iloc[-1])
                        open_p = float(hist['Open'].iloc[-1])
                        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else np.nan
                        change_abs = price - prev_close if not pd.isna(prev_close) else np.nan
                        change_pct = (change_abs / prev_close * 100) if not pd.isna(prev_close) else np.nan
                        result[asset] = {
                            'symbol_used': sym,
                            'status': 'available',
                            'price': price,
                            'open': open_p,
                            'previous_close': prev_close,
                            'change_abs': change_abs,
                            'change_pct': change_pct,
                            'source': 'history'
                        }
                        found = True
                        break
                except Exception:
                    continue
        if not found:
            result[asset] = {
                'symbol_used': symbols[0] if symbols else 'N/A',
                'status': 'indisponível',
                'price': np.nan,
                'open': np.nan,
                'previous_close': np.nan,
                'change_abs': np.nan,
                'change_pct': np.nan,
                'source': 'nenhuma'
            }
    return result
