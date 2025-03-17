
FROM python:3.11-slim

#Dependencias del dlib(Se demoran demasiado en instalar)
RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    make \
    python3-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    # <-- Instala el paquete de desarrollo de ZBar
    libzbar-dev \
    # <-- Asegura que las dependencias se resuelvan correctamente
    pkg-config \   
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

# Copiar todo el código del proyecto
COPY . .

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Crear directorios para base de datos SQLite y archivos estáticos (Cambiar en un futuro por Mysql o PostgreSQL)
RUN mkdir -p /app/db /app/static /app/media

EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 backend.wsgi:application"]

