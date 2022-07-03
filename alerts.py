import ccxt
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import requests
import config

exchange = ccxt.binance()

webhook = config.WEBHOOK_URL
bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='5m', limit=500)
df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

adx = df.ta.adx()
macd = df.ta.macd(fast=14, slow=28)
rsi = df.ta.rsi()

df = pd.concat([df, adx, macd, rsi], axis=1)
print(df)

last_row = df.iloc[-1]

print(last_row)

if last_row['ADX_14'] >= 25:
    if last_row['DMP_14'] > last_row['DMN_14']:
        message = f"STRONG UPTREND: The ADX is {last_row['ADX_14']:.2f}"
    elif last_row['DMN_14'] > last_row['DMP_14']:
        message = f"STRONG DOWNTREND: The ADX is {last_row['ADX_14']:.2f}"
    print(message)
if last_row['ADX_14'] < 25:
    message = f"NO TREND: The ADX is {last_row['ADX_14']:.2f}"
    print(message)

payload = {
    "username": "alertbot",
    "content":message
}

requests.post(webhook, json=payload)