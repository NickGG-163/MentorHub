FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY mentorhub/ ./mentorhub/
RUN python -m pip install .
COPY alembic.ini ./
COPY migrations/ ./migrations/
CMD ["uvicorn", "mentorhub.api:app", "--host", "0.0.0.0", "--port", "8000"]
USER 10001:10001