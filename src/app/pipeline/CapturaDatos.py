import requests
import pandas as pd
import json




async def api (api2):
    
    r = requests.get(api2)
    data = r.json()
    print(f"Data API: {data}")
    #respuestaIBM.json
    with open("respuestaAUDCAD.json", "w") as f:
        json.dump(data, f, indent=4)

    """with open('respuestaIBM.json', 'r') as f:
        data = json.load(f)
    """
    return data


async def normalizarData(time_series_key, api2 ):
    data = await api(api2)
    #print("Esta e data :", data)
    """with open('ejemploresult.json', 'r') as f:
        data = json.load(f)
    """
    ts_data = data[time_series_key]
    df = pd.DataFrame(ts_data).T
    
    
    df.index = pd.to_datetime(df.index, errors='coerce')
    df.index.name = "timestamp"
    df.sort_index(ascending=True, inplace=True)
  

    
    df = df.astype(float)
    df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    }, inplace=True)

    
    meta = data.get("Meta Data", {})
    symbol = meta.get("2. Symbol", "UNKNOWN")
    interval = meta.get("4. Interval", "UNKNOWN")
    df["symbol"] = symbol
    df["interval"] = interval


    
    df['return'] = df['close'].pct_change()
    df['diff_close_open'] = df['close'] - df['open']
    df['SMA_5'] = df['close'].rolling(window=5).mean()
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['EMA_5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

    
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    window_rsi = 14  
    avg_gain = gain.rolling(window=window_rsi, min_periods=window_rsi).mean()
    avg_loss = loss.rolling(window=window_rsi, min_periods=window_rsi).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal']

    
    window_bb = 20
    df['SMA_20'] = df['close'].rolling(window=window_bb).mean()
    df['STD_20'] = df['close'].rolling(window=window_bb).std()
    df['Upper_BB'] = df['SMA_20'] + 2 * df['STD_20']
    df['Lower_BB'] = df['SMA_20'] - 2 * df['STD_20']

    
    df['Volatility'] = df['return'].rolling(window=5).std()

    
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month

    
    df['close_lag1'] = df['close'].shift(1)
    df['close_lag2'] = df['close'].shift(2)

    
    df['target'] = df['close'].shift(-1)
    df['target_return'] = df['return'].shift(-1)

    
    return df

async def main(time_series, api2):
    data = await normalizarData(time_series, api2)
    return data
    

    
