FROM python:3.13-bullseye

# Establece el directorio de trabajo
WORKDIR /app

# Instala Poetry
RUN pip install --upgrade pip && \
    pip install poetry==2.1.1

# Copia el archivo de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instala dependencias sin crear un entorno virtual dentro del contenedor
RUN touch README.md
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copia el resto del proyecto
COPY . /app/

# Expone el puerto si usas Flask por defecto
EXPOSE 5000

# Comando por defecto (puedes ajustarlo según cómo inicies Flask)
ENV FLASK_APP=src/app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
