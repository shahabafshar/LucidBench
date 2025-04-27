FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y \
    fio \
    python3 \
    python3-pip \
    xfsprogs \
    btrfs-progs \
    e2fsprogs \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /benchmark /results

# Copy benchmark scripts
COPY src/benchmark/benchmark.py /benchmark/
COPY config/requirements.txt /benchmark/

# Install Python dependencies
RUN pip3 install -r /benchmark/requirements.txt

# Set working directory
WORKDIR /benchmark

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create volume for results
VOLUME ["/results"]

# Set entrypoint
ENTRYPOINT ["python3", "benchmark.py"] 