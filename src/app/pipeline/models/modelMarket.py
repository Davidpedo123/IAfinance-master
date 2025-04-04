import requests

class MarketStackConfig:
    """
    Clase de configuración para la API de MarketStack.
    Permite encapsular las variables sensibles y parámetros de consulta.
    """
    def __init__(self, access_key: str, symbols: str, date_from: str, date_to: str):
        self.access_key = access_key
        self.symbols = symbols
        self.date_from = date_from
        self.date_to = date_to

    def __repr__(self):
        return f"<MarketStackConfig symbols={self.symbols}, date_from={self.date_from}, date_to={self.date_to}>"

class MarketStackClient:
    """
    Cliente para interactuar con la API de MarketStack.
    Recibe una instancia de MarketStackConfig para construir la URL y realizar la consulta.
    """
    BASE_URL = "http://api.marketstack.com/v1/eod"

    def __init__(self, config: MarketStackConfig):
        self.config = config

    def build_url(self, limit: int = None) -> str:
        """
        Construye la URL de consulta usando la configuración inyectada.
        Se puede incluir opcionalmente el parámetro 'limit'.
        """
        url = (
            f"{self.BASE_URL}?access_key={self.config.access_key}"
            f"&symbols={self.config.symbols}"
            f"&date_from={self.config.date_from}"
            f"&date_to={self.config.date_to}"
        )
        if limit is not None:
            url += f"&limit={limit}"
        return url

    def consulta_market(self, limit: int = None) -> dict:
        """
        Realiza la consulta a la API y retorna el JSON de respuesta.
        """
        url = self.build_url(limit)
        response = requests.get(url)
        response.raise_for_status()  # Se puede manejar o propagar la excepción
        return response.json()

# Ejemplo de uso:
if __name__ == "__main__":
    # Inyecta la configuración. Estos valores pueden venir, por ejemplo, de variables de entorno o un archivo de configuración.
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
