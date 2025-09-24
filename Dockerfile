# Imagen base de Python
FROM python:3.12-slim

# Instalar dependencias necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la app
COPY . .

# Exponer puerto (Django usa 8000 por defecto)
EXPOSE 8000

# Comando de arranque de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
