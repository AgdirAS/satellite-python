FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gdal-bin \
        libgdal-dev \
        build-essential \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install numpy first, then rasterio with --no-build-isolation so it builds
# against the installed numpy rather than trying to fetch numpy==2.0.0rc1
# (a yanked RC that rasterio's build system incorrectly pinned)
RUN pip install --no-cache-dir numpy==1.26.4 && \
    pip install --no-cache-dir --no-build-isolation rasterio
