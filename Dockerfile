FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

ENV PORT 8080

EXPOSE ${PORT}

ENTRYPOINT streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0 --server.baseUrlPath=/demo