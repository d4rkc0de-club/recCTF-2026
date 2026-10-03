FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY model.pkl .
COPY templates ./templates

EXPOSE 5021

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5021", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "30", \
     "app:app"]