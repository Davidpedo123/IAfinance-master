async def fetch_data(self):
        
        url = f"{self.base_url}?function={self.function}&symbol={self.symbol}&outputsize=full&apikey={self.api_key}"
        response = requests.get(url)
        
        data = response.json()
        return data