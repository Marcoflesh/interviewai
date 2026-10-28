# RN-12 / RNF-09: version EXACTA de Python. NO usar tags flotantes (latest, 3, 3.12).
# NOTA: este Dockerfile NO se ha construido aun (T-001 lo valida con `docker compose build`).
FROM python:3.12.7-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
