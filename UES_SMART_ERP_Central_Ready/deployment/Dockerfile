FROM python:3.12-slim
WORKDIR /app
COPY backend/cloud/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend/cloud /app/backend/cloud
COPY backend/src/server.py /app/backend/src/server.py
COPY database/schema.sql /app/database/schema.sql
COPY frontend/dist /app/frontend/dist
ENV PYTHONUNBUFFERED=1 UES_FRONTEND_PATH=/app/frontend/dist UES_REQUIRE_POSTGRES=true
CMD ["sh", "-c", "uvicorn backend.cloud.app:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
