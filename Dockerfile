# Python 3.10 asosidagi rasm
FROM python:3.10-slim

# Konteyner ichida ishchi katalog
WORKDIR /app

# Loyiha fayllarini konteynerga ko‘chirish
COPY . .

# Kerakli kutubxonalarni o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "bot/main.py"]
