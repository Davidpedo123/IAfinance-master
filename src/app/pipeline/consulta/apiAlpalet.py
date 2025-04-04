async def fetch_data(self):
        # Construimos la URL con los parámetros
        url = f"{self.base_url}?function={self.function}&symbol={self.symbol}&outputsize=full&apikey={self.api_key}"
        response = requests.get(url)
        # Se podría agregar manejo de errores aquí
        data = response.json()
        return data