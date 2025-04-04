from pipeline.CapturaDatos import main
from modelPredict.LSTM import hybrid_forecast
from env.config import url

async def model_train(symbol):
    api2 = url.build_url(symbol=symbol)
    data = await main(time_series="Time Series (1min)", api2=api2)
    data_train = hybrid_forecast(df=data, forecast_steps=12)
    return data_train