import os

API = os.environ.get('API', "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=2S09HBNYQ5UZRPYM")


class url:
    @staticmethod
    def build_url(
        symbol="USDMXN",
        interval="1min",
        function="TIME_SERIES_INTRADAY",
        key="NWWSH6Y32NF7Z20B"
    ):
        api2 = (
            f"https://www.alphavantage.co/query?"
            f"function={function}&symbol={symbol}&interval={interval}"
            f"&outputsize=full&apikey={key}"
        )
        return api2
        
    