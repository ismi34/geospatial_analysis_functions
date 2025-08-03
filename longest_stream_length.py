import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge
from pathlib import Path

def channel_length(catchment_shp_path, stream_shp_path, outpath, id_column=None):
    """
    Parameters:
        catchment_shp_path (str or Path): Path to catchment shapefile
        stream_shp_path (str or Path): Path to stream shapefile (already clipped or full)
        outpath (str or Path): Folder where CSV will be saved
        id_column (str): Name of the column in the catchment file that uniquely identifies each catchment

    Output:
        Saves a CSV file named 'channel_length.csv' in the given outpath containing:
        - catchment_id
        - longest_stream (in meters)
    """
    #load the data
    catchments = gpd.read_file(Path(catchment_shp_path))
    streams = gpd.read_file(Path(stream_shp_path))
    id_column = str(id_column)

    outpath = Path(outpath)
    outpath.mkdir(parents=True, exist_ok=True)
    
    if id_column is None or id_column not in catchments.columns:
        raise ValueError(f"Invalid or missing id_column: '{id_column}' not found in catchment shapefile.")

    #crs check
    if streams.crs != catchments.crs:
        streams = streams.to_crs(catchments.crs)

    #looping through catchments and filter corresponding streams
    results = []

    
    for idx, catch in catchments.iterrows():
        catch_id = catch[id_column]
        catch_geom = catch.geometry

        # Use .intersection instead of .within to catch overlapping streams
        local_stream = streams[streams.intersects(catch_geom)]

        lines = []
        for geom in local_stream.geometry:
            if geom is None:
                continue
            elif geom.geom_type == 'LineString':
                lines.append(geom)
            elif geom.geom_type == 'MultiLineString':
                lines.extend(geom.geoms)

        if lines:
            merged = linemerge(lines)
            if isinstance(merged, MultiLineString):
                longest = max(list(merged.geoms), key=lambda x: x.length)
            else:
                longest = merged
            length = np.round(longest.length)
        else:
            length = 0.0

        results.append({
            "catchment_id": catch_id,
            "longest_stream_m": length
        })

            
    df = pd.DataFrame(results)
    df.to_csv(outpath / "channel_length.csv", index=False)
    print(f"Saved channel length report to: {outpath / 'channel_length.csv'}")