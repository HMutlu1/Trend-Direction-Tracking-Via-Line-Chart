from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from binance.client import Client
import plotly.graph_objects as go
# Binance API anahtarlarınızı buraya ekleyin
api_key = 'Your_API_Key'
api_secret = 'Your_API_Secret'
client = Client(api_key, api_secret)

# İlgilendiğiniz ticaret çiftleri
symbols = ['BTCUSDT', 'AVAXUSDT']

for symbol in symbols:
    klines = client.get_klines(symbol=symbol, interval='15m', limit=65)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

    # Kapanış fiyatları üzerinden trend analizi yapabilirsiniz (örneğin, basit bir hareketli ortalama kullanarak)
    df['close'] = pd.to_numeric(df['close'])
    df['MA15'] = df['close'].rolling(window=15).mean()

    # Son kapanış fiyatı ile 15 günlük hareketli ortalama arasındaki ilişkiyi kontrol edin
    last_close = df['close'].iloc[-1]
    last_ma15 = df['MA15'].iloc[-1]

    if last_close > last_ma15:
        trend_direction = 'up'
    elif last_close < last_ma15:
        trend_direction = 'down'
    else:
        trend_direction = 'horizontal'

    # Grafiği çiz
    plt.plot(df['timestamp'], df['close'], label='Closing price')
    plt.plot(df['timestamp'], df['MA15'], label='15 Day Moving Average')
    plt.title(f'Trading Pair: {symbol}, Trend Direction: {trend_direction}')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
