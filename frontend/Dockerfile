FROM python:3.12-slim

ENV ROOT_FOLDER=/rental-crud

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=${ROOT_FOLDER}

WORKDIR ${ROOT_FOLDER}

COPY pyproject.toml poetry.lock ./

# Install poetry
RUN pip install poetry

# Install only frontend dependencies
RUN poetry config installer.max-workers 10
RUN poetry install --only frontend --no-root --no-interaction --no-ansi

# Copy all frontend source (because build context = frontend/)
COPY . .

# Railway exposes a dynamic PORT
EXPOSE $PORT

# Run Streamlit on Railway's PORT
CMD ["sh", "-c", "poetry run streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT"]
