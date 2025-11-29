FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y git

# instalar bash y curl para codecov uploader (y ca-certificates)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
