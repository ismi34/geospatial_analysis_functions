import pandas as pd
import numpy as np
from pathlib import Path
import whitebox

def make_slope_raster(dem_dir, out_dir):

    wbt = whitebox.WhiteboxTools()

    dem_dir = Path(dem_dir)
    
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    dem_rasters = list(dem_dir.glob("*tif"))

    for file in dem_rasters:
        outfile = out_dir / f"{file.stem}_slope.tif"
        wbt.slope(
            file,
            outfile,
            units="percent"
        )
    print(f"Slope rasters are created for {len(dem_rasters)} DEMs")
    
