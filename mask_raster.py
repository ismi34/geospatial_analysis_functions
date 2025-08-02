import pandas as pd
import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from pathlib import Path
import os

def mask_raster(vector_path, raster_path, output_dir, id_column = None):

    vector_path = Path(vector_path) 
    raster_path = Path(raster_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok = True)

    gdf = gpd.read_file(vector_path)
    geom_list = list(gdf['geometry']) #raster will be clipped as per these geometry

    with rasterio.open(raster_path) as src:
        if gdf.crs != src.crs:
            gdf = gdf.to_crs(src.crs) #make sure both vector and raster in same CRS
        
        for i, geom in enumerate(geom_list):
            array, transform = mask(src, [geom], crop=True) #use the mask function to clip
            
            out_meta = src.meta.copy() #we need the raster metadata to write clipped radters
            out_meta.update({
                    "driver": "GTiff",
                    "height": array.shape[1],
                    "width": array.shape[2],
                    "transform": transform
            })
            
            #Determine filename
            if id_column and id_column in gdf.columns:
                name = gdf.iloc[i][id_column]
                name_str = str(name).replace(" ", "_")
                out_file = output_dir / f"{name_str}.tif"
            else:
                out_file = output_dir / f"{i+1}.tif"
            
            with rasterio.open(out_file, "w", **out_meta) as dest:
                dest.write(array)
                
    print(f"Saved {len(gdf)} clipped raster(s) to: {output_dir}")
        
        
        
    
    
    
    
    

