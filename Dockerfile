FROM python:3.12-slim

WORKDIR /app

COPY src/app/ .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r app/lib/requirements.txt


CMD ["streamlit", "run", "main.py"]
