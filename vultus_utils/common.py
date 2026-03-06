import numpy as np
import rasterio as rio
import json
import math
import re
from urllib.parse import urlparse
from scipy import stats
from pydantic import BaseModel
from typing import Type, TypeVar, List, Callable
from .validation import with_validation
from .logging import with_logger, Logger
from .s3_objects import *


def check_s3_file(bucket="", prefix="", /, url=None):
    if url is not None:
        s3_scheme, bucket, prefix, *_ = urlparse(url)
        prefix = prefix[1:] # remove leading `/`

    results = S3_CLIENT.list_objects(Bucket=bucket, Prefix=prefix)
    return "Contents" in results


def read_meta(band):
    with rio.open(band) as src:
        meta = src.profile.copy()
    return meta


def read_band(band):
    s3_scheme, bucket, key, *_ = urlparse(band)
    key = key[1:] # remove leading `/`
    # reading into `rio.MemoryFile` instead of using `rio.open` because `rio.open`
    # behaves like it caches the result, so in case of continuously changing files
    # like datamasks, `rio.open` returns outdated result  
    with rio.MemoryFile() as memfile:
        S3.Bucket(bucket).Object(key).download_fileobj(memfile)
        with memfile.open() as dataset:
            band = dataset.read(1).astype("float64")
    return band


def generate_tiff(meta, values, outputpath):
    with rio.open(str(outputpath), "w", **meta) as dst:
        dst.write(values, 1)
    return


def generate_stats(index, out_stats, date):
    arr = index[~np.isnan(index)]
    arr_min = np.min(arr)
    arr_max = np.max(arr)
    arr_mean = np.mean(arr)
    arr_median = np.median(arr)
    arr_std = np.std(arr)
    arr_var = np.var(arr)
    convert = date.split("T")
    k = {
        "date": str(convert[0]),
        "minimum": str(arr_min),
        "maximum": str(arr_max),
        "mean": str(arr_mean),
        "std": str(arr_std),
        "var": str(arr_var),
        "median": str(arr_median),
    }
    with open(out_stats, "w", encoding="utf-8") as f:
        json.dump(k, f, ensure_ascii=False, indent=4)
    return


def calculate_z_score(index):
    index = index[np.logical_not(np.isnan(index))]
    index = index[~np.isnan(index)]
    Z_score = stats.zscore(index)  # Calculate Z-Score value of  index
    ND = stats.norm.sf(abs(Z_score))  # Calculate Normal Distribution from Z-score of  index
    ND = ND.astype(float)
    return np.nanmean(ND)


def todB(linear):
    return linear * math.log(10, math.e) * 10


def angleNorm(value, angle):
    # Do angle normalization to a reference angle of 30 degrees
    # Van Tricht, K., Gobin, A., Gilliams, S., & Piccard, I. (2018). Eq.1
    return (
        value * (np.cos(30 * math.pi / 180) ** 2)
        /
        (np.cos(angle * math.pi / 180) ** 2)
    )


def get_s3_files_by_re(client, bucket, prefix, regex: re.Pattern) -> List[str]:
    objects = client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if "Contents" not in objects:
        return []
    
    result = list()
    for record in objects["Contents"]:
        if regex.match(record["Key"]) is not None:
            result.append(record["Key"])

    return result


M = TypeVar("M", bound=BaseModel)
R = TypeVar("R")

def with_validation_and_logger(model: Type[M], service: str):
    def wrapper(func: Callable[[M, Logger], R]) -> Callable[[dict], R]:
        func_with_validation = with_validation(model)(func)
        return with_logger(service)(func_with_validation)
    return wrapper
