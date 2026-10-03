FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MODEL_FILE=/app/challenge_filtered.model \
    HINT_KEY=a4dw-wd31-wwe32-dd24 \
    FLAG=d4rk{pr0bability_1s_A_f03}

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY static ./static

# Put challenge_filtered.model next to this Dockerfile before building.
COPY challenge_filtered.model .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5066

CMD ["gunicorn", "--bind", "0.0.0.0:5066", "--workers", "1", "--threads", "4", "--timeout", "30", "--access-logfile", "-", "app:app"]
