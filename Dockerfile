FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gdal-bin \
        libgdal-dev \
        build-essential \
        pkg-config \
        cython3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "setuptools<80" numpy rasterio

WORKDIR /app
COPY pyproject.toml .
COPY vultus_utils/ ./vultus_utils/
RUN pip install --no-cache-dir .
