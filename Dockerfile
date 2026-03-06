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

ARG SEQ_URL
ARG S3_BUCKET
ENV SEQ_URL=${SEQ_URL} \
    S3_BUCKET=${S3_BUCKET}

WORKDIR /app
COPY pyproject.toml .
COPY vultus_utils/ ./vultus_utils/
RUN pip install --no-cache-dir .
