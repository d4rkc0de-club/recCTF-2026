FROM python:3.10-slim

# Install system dependencies and socat
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install gensim and numpy
RUN pip install --no-cache-dir gensim numpy

# Copy challenge files
COPY word_challenge.py challenge_filtered.model /app/

# Expose port for this challenge
EXPOSE 1338

# Run via socat
CMD ["socat", "TCP-LISTEN:1338,reuseaddr,fork", "EXEC:python3 word_challenge.py"]