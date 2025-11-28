FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install

COPY . .

CMD ["python", "app.py"]
