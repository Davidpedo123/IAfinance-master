# Guia rapida del modelo 

## Tiene dos opciones ejecutarlo mediante docker o via terminal con streamlit

Sin docker solo bastaria generar un entorno virtual en caso de que no quiera conflicto con sus dependencias

`python -m virtualenv [nombre_entorno]`

posterior nos dirigiremos a la carpeta `src/app` y ejecutaremos `pip install -r lib/requirements.txt`
para instalar todas las dependencias ( antes de esto hay que activar el entorno virutal en Script/activate)

Ya las dependencias instaladas debemos dirigirnos a la carpeta app y ejecutar el servidor de streamlit con
`python -m streamlit run main.py` Y ya estaria expuesto nuestro modelo

# Guia de uso:

En el apartado del input donde se escribe el symnbolo si es un par de divisas, tienes que escribir pegado, ejemplo `USDEUR`

# Guia de configuracion

Para la configuracion sera un poco mas compleja porque se tendra que dirigir a la documentacion de aplha vantage, 
https://www.alphavantage.co/documentation/

Para configurar los intervalos podriamos ir al `env/config` 

```python
class url:
    @staticmethod
    def build_url(
        symbol="USDMXN",
        interval="1min",
        function="TIME_SERIES_INTRADAY",
        key=key
    ):
        api2 = (
            f"https://www.alphavantage.co/query?"
            f"function={function}&symbol={symbol}&interval={interval}"
            f"&outputsize=full&apikey={key}"
        )
        return api2
```
Hay parametros que deben ir juntos hay funciones que no llevan intervalos por eso hay q leer la documentacion

En el modulo `controller/funciones.py` estara el orquestador de todo el valor de time_series es constante, y es dependiente a la respuesta de la API,
este time series puede cambiar seguna la funcion y intervalos

```python

async def model_train(symbol):
    api2 = url.build_url(symbol=symbol)
    data = await main(time_series="Time Series (1min)", api2=api2)
    data_train = hybrid_forecast(df=data, forecast_steps=12)
    return data_train

```

## Con docker

Solo ejecutamos desde la carpeta raiz, `docker build -t {nombre_imagen} .` y ejecutamos el docker run, en el puerto que deseamos el puerto en el que se expone en la imagen es en el `8501` , deberian ejecutar `docker run -p 127.0.0.1:8501:8501 {nombre_imagen}` .
