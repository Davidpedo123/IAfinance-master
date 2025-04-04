from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

with Diagram("Flujo Modelo Híbrido ARIMA-LSTM", show=False):
    entrada = Custom("Data Input\n(df con 'close', 'symbol', 'interval')", "input.png")
    
    with Cluster("Preprocesamiento"):
        validacion = Custom("Validar columnas\n['close','symbol','interval']", "checklist.png")
        calc_timedelta = Custom("Calcular\ninterval_timedelta", "clock.png")
    
    with Cluster("Modelado ARIMA"):
        arima = Custom("ARIMA(1,1,1)", "arima.png")
        residuos = Custom("Calcular residuos\n(close - arima_pred)", "math.png")
    
    with Cluster("Modelado LSTM"):
        escalado = Custom("Escalar residuos\n(MinMaxScaler)", "scaler.png")
        secuencias = Custom("Crear secuencias\n(time_steps=6", "layers.png")
        lstm = Custom("Entrenar LSTM\n(LSTM(50) + Dense(1))", "lstm.png")
    
    prediccion = Custom("Pronóstico combinado\n(ARIMA + LSTM)", "forecast.png")
    salida = Custom("Formateo de resultados\n(Decimal precision)", "output.png")

    entrada >> validacion >> calc_timedelta >> arima
    arima >> residuos >> escalado >> secuencias >> lstm
    lstm >> prediccion
    calc_timedelta >> Edge(color="transparent") >> prediccion
    prediccion >> salida