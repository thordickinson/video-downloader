# Imagen base con Python 3.11 slim
FROM python:3.12-slim

# Variables
ENV DOWNLOAD_DIR=/root/.video_downloader
ENV PORT=5000

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia el código
COPY app.py .

# Instala dependencias de Python
RUN pip install --no-cache-dir fastapi uvicorn yt-dlp

# Expone el puerto
EXPOSE ${PORT}

# Ejecuta la app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
