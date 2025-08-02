import pandas as pd
import numpy as np
import rasterio
from pathlib import Path
import os

def make_raster_stat(raster_dir, output_dir, outfile_name = None):
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if outfile_name is None:
        outfile_name = "raster_statistics"
    else:
        outfile_name = str(outfile_name)
    
    raster_dir = Path(raster_dir)
    raster_files = list(raster_dir.glob("*.tif"))

    max_values = []
    min_values = []
    mean_values = []
    std_devs = []
    ids = []
    keys = ['catchment_id', 'min', 'max', 'mean', 'std_dev']

    for file in raster_files:
        with rasterio.open(file) as src:
            
            #filter out the nodata value
            nodata = src.nodata
            raw_array = src.read(1)
            array = raw_array[raw_array != nodata]
            
            ids.append(file.stem)
            
            #calculate the stats
            mean_values.append(np.round(np.mean(array), 2))
            
            max_values.append(np.round(np.max(array), 2))
            
            min_values.append(np.round(np.min(array), 2))
            
            std_devs.append(np.round(np.std(array), 2))

    #make a DataFrame
    df = pd.DataFrame(zip(ids, min_values, max_values, mean_values, std_devs), columns=keys)
    df.to_csv(output_dir / f"{outfile_name}.csv", index=False)
    
    print(f"Statistics of {len(raster_files)} raster files are saved in {output_dir}")
    return df