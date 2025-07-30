def merge_rasters(input_raster_directory, output_raster_directory):
    
    import rasterio
    from rasterio.merge import merge
    import os
    from pathlib import Path

    raster_dir = Path(input_raster_directory)
                        #path to the folder where split rasters are hosted
    output_merged_raster = Path(output_raster_directory) / 'merged_raster.tif'

    raster_files = [file for file in os.listdir(raster_dir) if file.endswith('.tif')]

    if not raster_files:
        raise ValueError("Error: Your raster directory is empty!")
    else:
        open_rasters = [] #merge function need raster in open mode, thus we put them open in this list
        for file in raster_files:
            open_raster = rasterio.open(os.path.join(raster_dir, file))
            open_rasters.append(open_raster)
        
        merged_array, transform = merge(open_rasters)
                                    #merge function return a numpy array and transform, we then write raster from the array
        meta_data = open_rasters[0].meta.copy() #we need meta data to write raster from numpy array
                                                #but we need to update the shape, transform, driver
        meta_data.update({
            'height': merged_array.shape[1],
            'width': merged_array.shape[2],
            'transform': transform,
            'driver': 'GTiff'
            })
        
        #write the array into raster using the metadata
        with rasterio.open(output_merged_raster, 'w', **meta_data) as dest:
            dest.write(merged_array)
        
        for open_raster in open_rasters:
            open_raster.close()
        
                                            
    
    
    