# Imagen de Python
FROM python:3.11-slim


WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        python3-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*



COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app


EXPOSE 8000

# Comando para levantar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


