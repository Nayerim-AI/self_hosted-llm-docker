FROM python:3.10-slim

# Install dependensi sistem
RUN apt-get update && \
    apt-get install -y \
        git build-essential cmake \
        libcurl4-openssl-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files

COPY main.py .

COPY personas.json .
COPY build_llama.sh /app/build_llama.sh
RUN chmod +x build_llama.sh && /app/build_llama.sh

# Install python dependencies
# Install dependencies (non-PyTorch)
RUN pip install flask flask-cors \
    wikipedia \
    --default-timeout=100 google-api-python-client pandas \
    transformers==4.51.3 \
    python-dotenv \
    llama-cpp-python

# Install PyTorch dari index khusus CPU
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu


# Jalankan Flask API
CMD ["python", "main.py"]
