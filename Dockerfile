FROM python:3.12.4

RUN pip install poetry==1.8.3

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY . .
RUN poetry install --without dev --no-root

RUN chmod 755 .
#RUN poetry run poetry run alembic upgrade head

#CMD ["fastapi", "run", "app/app.py"]