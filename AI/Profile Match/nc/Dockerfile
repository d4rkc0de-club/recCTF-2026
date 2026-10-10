FROM python:3.10-slim

# Install socat to expose the python script over a TCP port
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy challenge files into the container
COPY challenge.py model.pkl /app/

# Expose the port the challenge will run on
EXPOSE 1337

# Run the python script via socat
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 challenge.py"]