import numpy as np


REFLECTANCE_CONSTANT = 10000


def calc_ndvi(red_value, nir_value):
    red = red_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir - red
    b = nir + red
    ndvi = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return ndvi


def calc_gndvi(green_value, nir_value):
    green = green_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir - green
    b = nir + green
    gndvi = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return gndvi


def calc_ndre(red_edge_value, nir_value):
    red_edge = red_edge_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir - red_edge
    b = nir + red_edge
    ndre = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return ndre


def calc_evi(red_value, blue_value, nir_value):
    red = red_value / REFLECTANCE_CONSTANT
    blue = blue_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir - red
    b = (nir + 6.0 * red - 7.5 * blue) + 1.0
    evi = 2.5 * np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return evi


def calc_evi2(red_value, nir_value):
    red = red_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir - red
    b = nir + 2.4 * red + 1
    evi2 = 2.5 * np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return evi2


def calc_rvi(red_value, nir_value):
    red = red_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir
    b = red
    rvi = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return rvi


def calc_ndwi(swir_value, nir_value):
    swir = swir_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    a = nir - swir
    b = nir + swir
    ndwi = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return ndwi


def calc_msavi2(red_value, nir_value):
    red = red_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    msavi2 = (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2
    return msavi2


def calc_lai(red_value, nir_value):
    red = red_value / REFLECTANCE_CONSTANT
    nir = nir_value / REFLECTANCE_CONSTANT
    lai = 10.22 * (nir - 1.35 * red) + 0.4768
    return lai


def calc_s2rep2(b_04_value, b_05_value, b_06_value, b_07_value):
    b_04 = b_04_value / REFLECTANCE_CONSTANT
    b_05 = b_05_value / REFLECTANCE_CONSTANT
    b_06 = b_06_value / REFLECTANCE_CONSTANT
    b_07 = b_07_value / REFLECTANCE_CONSTANT
    a = 705 + 35 * (0.5 * (b_07 + b_04) - b_05)
    b = b_06 - b_05
    s2rep2 = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    return s2rep2


def calc_redvi2(b_06_value, b_08a_value):
    b_06 = b_06_value / REFLECTANCE_CONSTANT
    b_08a = b_08a_value / REFLECTANCE_CONSTANT
    redvi2 = b_08a - b_06
    return redvi2


def calc_mcari13(b_03_value, b_07_value, b_08a_value):
    b_03 = b_03_value / REFLECTANCE_CONSTANT
    b_07 = b_07_value / REFLECTANCE_CONSTANT
    b_08a = b_08a_value / REFLECTANCE_CONSTANT
    mcari13 = ((b_08a - b_07) - 0.2 * (b_08a - b_03)) * (
        np.divide(b_08a, b_07, out=np.full_like(b_08a, np.nan), where=b_07 != 0)
    )
    return mcari13
