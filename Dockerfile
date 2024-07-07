FROM python:3.12.4

RUN pip install poetry==1.8.3

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY app ./app
RUN poetry install --without dev

RUN chmod 755 .

#CMD ["fastapi", "run", "app/app.py"]