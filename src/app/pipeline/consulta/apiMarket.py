


import requests as r
from models.modelMarket import MarketStackConfig as MSC
from env.config import key_m, symbols_m, date_from

config = MarketStackConfig(
        access_key="TU_API_KEY",
        symbols="AAPL",
        date_from="2021-01-01",
        date_to="2021-01-31"
    )
client = MarketStackClient(config)
data = client.consulta_market(limit=100)
print("Respuesta de la API:")
print(data)
