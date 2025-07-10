FROM python:3.10-slim

WORKDIR /app

COPY . .

# Qurish uchun kerakli tizim paketlari
RUN apt-get update && apt-get install -y gcc libffi-dev build-essential

# Python kutubxonalarni o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "bot/main.py"]


ENV PYTHONPATH=/app