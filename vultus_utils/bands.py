import numpy as np
from .common import read_band


BANDS = (
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "8A",
    "09",
    "11",
    "12",
)


def get_list_of_bands(date, storage_path=None):
    if not storage_path is None:
        return {
            band: storage_path + date + "_B{}_Clipped.tif".format(band)
            for band in BANDS
        }
    else:
        return {
            band: date + "_B{}_Clipped.tif".format(band)
            for band in BANDS
        }


def get_bands_mask(date, storage_path):
    bands = [
        read_band(band_path) 
        for band_path in get_list_of_bands(date, storage_path).values()
    ]
    bands_sum = np.sum(bands, axis=0)
    return np.where(bands_sum == 0, np.nan, 1)


try:
    import matplotlib as mpl
    from typing import Tuple

    def pixels_with_datamask(
        colormap: mpl.colors.Colormap,
        data_to_draw,
        mask,
        original_data_mask = None,
        missing_rbg: Tuple[float, float, float, float] = (1, 0, 0, 1),  # red by default
        outside_rbg: Tuple[float, float, float, float] = (0, 0, 0, 0),  # transparent by default
    ):
        if original_data_mask is None:
            original_data_mask = data_to_draw
        colors_data = colormap(data_to_draw)
        colors_data = np.where(
            np.isnan(original_data_mask)[:, :, np.newaxis] == True, 
            missing_rbg,
            colors_data
        )
        colors_data = np.where(
            np.isnan(mask)[:, :, np.newaxis] == True, 
            outside_rbg,
            colors_data
        )
        return colors_data

# in packages that have no matplotlib dependency
except ImportError:
    pass
