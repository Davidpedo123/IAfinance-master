import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from consulta.apiMarket import 
def normalizarMarket(data):
    """
    Extrae y normaliza las variables necesarias a partir del JSON para:
      - ARIMA: df['close'], order (p,d,q), df['interval'], metadato df['symbol'].
      - LSTM: Se provee el objeto escalador, la longitud de secuencia (time_steps) y la configuración del modelo
               (neurons, activation, epochs, batch_size).
    
    Se sigue el principio de solo servir la data, sin realizar cálculos o simulaciones de residuales.
    """
    with open("jsonexampleMarket.json", "r") as f:
        data_json = json.load(f)
    
    data = data_json["data"]
    df = pd.DataFrame(data)
    
    
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.set_index('date', inplace=True)
    
    
    df['close'] = df['close'].astype(float)
    
    
    symbol = df['symbol'].iloc[0]
    df['symbol'] = symbol
    
    
    df['interval'] = "1D"
    
    
    order = (1, 1, 1)
    
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    
    time_steps = 10
    
    
    lstm_config = {
        "neurons": 50,
        "activation": "tanh",
        "epochs": 50,
        "batch_size": 32
    }
    
    return {
        "df": df,
        "order": order,
        "scaler": scaler,
        "time_steps": time_steps,
        "lstm_config": lstm_config
    }

