from re import L
import ccxt
import pandas as pd

exchange = ccxt.binanceus()

bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1d', limit=365)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')


# Calculating true range on a datafram
def tr(df):
    df['prev close'] = df['close'].shift(1)
    df['h-l'] = df['high'] - df['low']
    df['h-pc'] = abs(df['high'] - df['prev close'])
    df['l-pc'] = abs(df['low'] - df['prev close'])
    tr = df[['h-l', 'h-pc', 'l-pc']].max(axis=1)
    return tr

# Calculating average TR
def atr(df, period=14):
    df['tr'] = tr(df)
    atr_val = df['tr'].rolling(period).mean()

    return atr_val

# Calculating supertrend
def supertrend(df, period=7, multiplier=3):
    df['atr'] = atr(df, period=period)
    # Basic upper band = (high + low) / 2 + (some multiplier * atr)
    df['upperband'] = ((df['high'] + df['low']) / 2) + (multiplier * df['atr'])
    # Basic lower band = (high + low / 2) - (some multiplier * atr)
    df['lowerband'] = ((df['high'] + df['low']) / 2) - (multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]
            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
    print(df)
    #return df
supertrend(df, period=5, multiplier=3)

#print(supertrend(df, period=5, multiplier=3))


