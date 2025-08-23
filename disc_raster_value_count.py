import rasterio
import geopandas as gpd
import numpy as np 
from pathlib import Path
import pandas as pd 


def disc_count(raster_path):
    """_summary_

    Args:
        raster_path (_type_): path to raster file as string or Path object
        output_dir (_type_): path to output directory as string or Path object
        outfile_name (str, optional): _description_. Defaults to "raster".
    Returns:
        Creates a csv file with value counts of the raster
        return none
    """
    with rasterio.open(raster_path) as src:
        arr_raw = src.read() 
        nodata = src.nodata
        arr = arr_raw[arr_raw != nodata]
        unique, counts = np.unique(arr, return_counts=True)
        value_counts = dict(zip(unique, counts))
        df = pd.DataFrame({'type': unique, 'count': counts})
        return df 
    
    