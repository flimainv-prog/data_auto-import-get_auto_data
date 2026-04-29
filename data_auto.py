import yfinance as yf

def _get_asset_data(symbols):
    for sym in symbols:
        # Try history
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period='2d')
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
                open_price = float(hist['Open'].iloc[-1])
                if len(hist) > 1:
                    prev_close = float(hist['Close'].iloc[-2])
                else:
                    prev_close = float('nan')
                change_abs = price - prev_close
                change_pct = (change_abs / prev_close * 100) if prev_close == prev_close else float('nan')
                return {
                    'symbol_used': sym,
                    'status': 'success',
                    'price': price,
                    'open': open_price,
                    'previous_close': prev_close,
                    'change_abs': change_abs,
                    'change_pct': change_pct,
                    'source': 'history'
                }
        except Exception:
            pass

        # Try info
        try:
            ticker = yf.Ticker(sym)
            info = ticker.info
            price = None
            if 'regularMarketPrice' in info:
                price = float(info['regularMarketPrice'])
            elif 'currentPrice' in info:
                price = float(info['currentPrice'])
            elif 'bid' in info:
                price = float(info['bid'])
            elif 'ask' in info:
                price = float(info['ask'])
            if price is not None:
                open_price = float(info.get('regularMarketOpen', float('nan')))
                prev_close = float(info.get('regularMarketPreviousClose', float('nan')))
                change_abs = float(info.get('regularMarketChange', float('nan')))
                change_pct = float(info.get('regularMarketChangePercent', float('nan')))
                return {
                    'symbol_used': sym,
                    'status': 'success',
                    'price': price,
                    'open': open_price,
                    'previous_close': prev_close,
                    'change_abs': change_abs,
                    'change_pct': change_pct,
                    'source': 'info'
                }
        except Exception:
            pass

        # Try download
        try:
            dl = yf.download(sym, period='2d', progress=False)
            if not dl.empty:
                price = float(dl['Close'].iloc[-1])
                open_price = float(dl['Open'].iloc[-1])
                if len(dl) > 1:
                    prev_close = float(dl['Close'].iloc[-2])
                else:
                    prev_close = float('nan')
                change_abs = price - prev_close
                change_pct = (change_abs / prev_close * 100) if prev_close == prev_close else float('nan')
                return {
                    'symbol_used': sym,
                    'status': 'success',
                    'price': price,
                    'open': open_price,
                    'previous_close': prev_close,
                    'change_abs': change_abs,
                    'change_pct': change_pct,
                    'source': 'download'
                }
        except Exception:
            pass

    return {
        'symbol_used': None,
        'status': 'no data available',
        'price': float('nan'),
        'open': float('nan'),
        'previous_close': float('nan'),
        'change_abs': float('nan'),
        'change_pct': float('nan'),
        'source': None
    }

def get_auto_data():
    data = {}
    data['WDO'] = _get_asset_data(['USDBRL=X', 'BRL=X'])
    data['DXY'] = _get_asset_data(['DX-Y.NYB', 'DX=F', 'DXY'])
    data['6L'] = _get_asset_data(['6L=F', 'GBPUSD=X', 'GBP=X'])
    return data
