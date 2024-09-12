# Use Python slim image for a lightweight base
FROM python:3.9-slim

RUN chmod 1777 /tmp

ENV PYTHONUNBUFFERED=1

# Install necessary dependencies (mostly for nsjail)
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    git \
    g++ \
    libnl-route-3-dev \
    libprotobuf-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/google/nsjail.git \
    && cd nsjail && make && mv /nsjail/nsjail /usr/local/bin \ 
    && rm -rf -- /nsjail

# Copy the app files to the working directory
COPY . /app
WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app

USER appuser

# Install Python dependencies from requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8080

# Start the Flask app
CMD ["python", "src/app.py"]
