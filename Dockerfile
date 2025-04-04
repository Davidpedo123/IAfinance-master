FROM python:3.12-slim

WORKDIR app

COPY src/app/ app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r lib/requirements.txt


RUN python3 -m streamlit run main.py