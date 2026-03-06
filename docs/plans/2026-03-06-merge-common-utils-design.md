# Design: Merge vultus-utils into satellite-python base image

**Date:** 2026-03-06
**Status:** Approved

## Problem

`vultus-utils` (from `vultus-core-application__common-utils`) is a shared Python library used by 11 downstream microservices. Currently each service Dockerfile manually copies and installs it from the build context:

```dockerfile
COPY common-utils ./common-utils
RUN pip install --no-cache-dir ./common-utils && rm -rf ./common-utils
```

This is repetitive, fragile, and couples every service build to carrying the common-utils directory in its build context.

## Solution (Option A: Bake into base image)

Include `vultus_utils` package source in the `satellite-python` repo and install it as part of the base image build. Downstream services get it automatically via `FROM ghcr.io/agdiras/satellite-python:latest`.

## Changes

### satellite-python repo
- Add `vultus_utils/` source directory (from common-utils)
- Add `pyproject.toml` (from common-utils)
- Update `Dockerfile` to install `vultus-utils` from local source after the GDAL layer

### vultus-core-application repo (11 services)
Remove from each Dockerfile:
```dockerfile
COPY common-utils ./common-utils
RUN pip install --no-cache-dir ./common-utils && rm -rf ./common-utils
```
Affected: bio_mass, crude_protein, disease_prediction, download, drymatter, historic_gap_filling, leaf_nitrogen, nitrogen_zoning, potato_analysis, soil_moisture, soil_organic_carbon, vegetation_indices

### vultus-core-application__common-utils repo
- Add deprecation notice to README
- Archive the repo on GitHub

## Build order after change

```
satellite-python → ghcr.io/agdiras/satellite-python:latest (includes vultus-utils)
  └── all 11 downstream services FROM that image
```

Future vultus-utils updates: commit to satellite-python → base image rebuilds → downstream picks up on next build.
