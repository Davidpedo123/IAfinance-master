import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from decimal import Decimal, getcontext
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf


def hybrid_forecast(df, forecast_steps=1, time_steps=6, start_time=None):
    """
    Realiza una predicción híbrida combinando ARIMA y LSTM sobre la columna 'close' de un DataFrame.

    Parámetros:
      - df: DataFrame con un índice datetime y una columna 'close'
      - forecast_steps: Número de pasos/intervalos a pronosticar
      - time_steps: Número de pasos usados para secuencias en LSTM
      - start_time: Momento inicial para las predicciones (si no se provee, se usa el último timestamp del df)

    Retorna:
      - Un diccionario JSON-like con las predicciones
    """
    
    
    required_columns = ['close', 'symbol', 'interval']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Falta la columna requerida: {col}")

    symbol = df['symbol'].iloc[0]
    interval = df['interval'].iloc[0]

    
    interval_timedelta = pd.to_timedelta(interval)

    
    model_arima = ARIMA(df['close'], order=(2, 1, 2))  
    model_arima_fit = model_arima.fit()
    
    df['arima_pred'] = model_arima_fit.predict(start=0, end=len(df)-1, dynamic=False)
    df['arima_resid'] = df['close'] - df['arima_pred']

    
    PIP_MULTIPLIER = 10000  
    residuals_pips = df['arima_resid'].dropna().values.reshape(-1, 1) * PIP_MULTIPLIER
    
    
    scaler = MinMaxScaler(feature_range=(-1, 1))  
    residuals_scaled = scaler.fit_transform(residuals_pips)

    # --- LSTM ---
    def create_sequences(data, time_steps):
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i:i+time_steps])
            y.append(data[i+time_steps])
        return np.array(X), np.array(y)

    X, y = create_sequences(residuals_scaled, time_steps)
    split = int(len(X) * 0.8)  
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    model_lstm = Sequential([
        LSTM(100, activation='tanh', recurrent_activation='sigmoid', 
             input_shape=(time_steps, 1), return_sequences=False),
        Dense(50, activation='tanh'),
        Dense(1, activation='linear')
    ])
    
    
    def pip_loss(y_true, y_pred):
        return tf.reduce_mean(tf.square(y_true - y_pred)) * 10000   
    
    model_lstm.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                      loss=pip_loss)  

    
    es = EarlyStopping(monitor='val_loss', patience=15,             restore_best_weights=True)
    model_lstm.fit(X_train, y_train, validation_data=(X_test, y_test), 
                  epochs=300, batch_size=32, callbacks=[es], verbose=0)

  
    arima_forecast = model_arima_fit.forecast(steps=forecast_steps)
    
    
    last_seq = residuals_scaled[-time_steps:].reshape(1, time_steps, 1)
    lstm_forecast_scaled = []
    
    for _ in range(forecast_steps):
        pred = model_lstm.predict(last_seq, verbose=0)
        lstm_forecast_scaled.append(pred[0, 0])
        last_seq = np.concatenate([last_seq[:, 1:, :], pred.reshape(1, 1, 1)], axis=1)
    
    lstm_forecast_pips = scaler.inverse_transform(np.array(lstm_forecast_scaled).reshape(-1, 1))
    lstm_forecast = lstm_forecast_pips / PIP_MULTIPLIER  

    
    final_forecast = arima_forecast.values.flatten() + lstm_forecast.flatten()


    if start_time is None:
        
        start_time = pd.to_datetime(df.index[-1]) + pd.to_timedelta(interval)
        print("Último timestamp en los datos:", df.index[-1])


    future_timestamps = pd.date_range(start=start_time, periods=forecast_steps, freq=pd.to_timedelta(interval))
    from decimal import Decimal, getcontext
    predictions_list = []
    margin = Decimal('0.5') if forecast_steps <= 3 else Decimal('1.0')
    last_close = Decimal(str(df['close'].iloc[-1]))
    


    getcontext().prec = 28


    predictions_list = []
    last_close = Decimal(str(df['close'].iloc[-1]))

    for ts, pred in zip(future_timestamps, final_forecast):
        
        pred_decimal = Decimal(str(pred))
        
        
        margin = Decimal('0.0005') if forecast_steps <= 3 else Decimal('0.001')
        confidence_adjustment = Decimal('0.0002')
        
        
        predicted_range = {
            "min": pred_decimal - margin,
            "predicted": pred_decimal,
            "max": pred_decimal + margin
        }

        
        change = ((pred_decimal - last_close) / last_close * 100)
        
        
        confidence_interval = {
            "lower": pred_decimal - margin - confidence_adjustment,
            "upper": pred_decimal + margin + confidence_adjustment
        }

        
        predictions_list.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "predicted_range": {
                "min": float(predicted_range["min"].quantize(Decimal('0.000000'))),
                "predicted": float(predicted_range["predicted"].quantize(Decimal('0.000000'))),
                "max": float(predicted_range["max"].quantize(Decimal('0.000000')))
            },
            "predicted_change": f"{change.quantize(Decimal('0.000000')):+}%",
            "confidence": 0.90,
            "confidence_interval": {
                "lower": float(confidence_interval["lower"].quantize(Decimal('0.000000'))),
                "upper": float(confidence_interval["upper"].quantize(Decimal('0.000000')))
            }
        })

        print(predictions_list)

    return {
        "symbol": symbol,
        "time_range": {
            "start": future_timestamps[0].strftime("%Y-%m-%d %H:%M:%S"),
            "end": future_timestamps[-1].strftime("%Y-%m-%d %H:%M:%S")
        },
        "interval": interval,
        "predictions": predictions_list
    }