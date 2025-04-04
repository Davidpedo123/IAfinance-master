from controller.funciones import model_train
import pandas as pd
import streamlit as st
from decimal import Decimal, getcontext
import plotly.graph_objects as go  

def flatten_prediction_data(predictions):
    flat_data = []
    for item in predictions:
        flat_item = {
            "timestamp": item["timestamp"],
            "predicted_min": float(Decimal(str(item["predicted_range"]["min"])).quantize(Decimal('0.000000'))),
            "predicted": float(Decimal(str(item["predicted_range"]["predicted"])).quantize(Decimal('0.000000'))),
            "predicted_max": float(Decimal(str(item["predicted_range"]["max"])).quantize(Decimal('0.000000'))),
            "predicted_change": item["predicted_change"],
            "confidence": item["confidence"],
            "confidence_lower": float(Decimal(str(item["confidence_interval"]["lower"])).quantize(Decimal('0.000000'))),
            "confidence_upper": float(Decimal(str(item["confidence_interval"]["upper"])).quantize(Decimal('0.000000')))
        }
        flat_data.append(flat_item)
    return flat_data

async def run_app():
    col1, col2 = st.columns([2, 1])
    with col1:
        symbol = st.text_input("Símbolo a analizar", placeholder="Ejemplo: USDMXN")
    
    analyze_btn = st.button("Analizar", type="primary")

    if analyze_btn and symbol:
        with st.spinner(f"Obteniendo datos de {symbol}..."):
            result = await model_train(symbol)
            
            if result and "predictions" in result:
                flat_predictions = flatten_prediction_data(result["predictions"])
                df = pd.DataFrame(flat_predictions)
                
                
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
                
                pd.options.display.float_format = '{:.6f}'.format
                
                
                st.write("### Resultado Detallado")
                st.dataframe(
                    df[['timestamp', 'predicted', 'predicted_min', 'predicted_max']].reset_index(drop=True),
                    height=300
                )
                
                
                st.write("### Análisis de Precisión Decimal")
                fig = go.Figure()
                
                
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['predicted'],
                    name='Predicción',
                    line=dict(color='#1f77b4', width=2),
                    hovertemplate="<b>%{x|%H:%M:%S}</b><br>Valor: %{y:.6f}<extra></extra>"
                ))
                
               
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['predicted_max'],
                    name='Máximo',
                    line=dict(color='#2ca02c', dash='dot'),
                    hovertemplate="Máx: %{y:.6f}<extra></extra>"
                ))
                
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['predicted_min'],
                    name='Mínimo',
                    line=dict(color='#d62728', dash='dot'),
                    hovertemplate="Mín: %{y:.6f}<extra></extra>"
                ))
                
                
                y_center = df['predicted'].mean()
                zoom_range = st.slider(
                    "Rango de visualización (±)",
                    min_value=0.0001,
                    max_value=0.0100,
                    value=0.0010,
                    step=0.0001,
                    format="%.4f"
                )
                
                
                fig.update_layout(
                    yaxis=dict(
                        range=[y_center - zoom_range, y_center + zoom_range],
                        tickformat=".6f",
                        gridcolor='lightgray'
                    ),
                    xaxis=dict(
                        tickformat="%H:%M:%S",
                        gridcolor='lightgray'
                    ),
                    hovermode="x unified",
                    height=500,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.success('Análisis de precisión completado!', icon="✅")
                
            else:
                st.warning("No se encontraron predicciones para mostrar.")
    elif analyze_btn and not symbol:
        st.warning("¡Por favor ingresa un símbolo válido!")