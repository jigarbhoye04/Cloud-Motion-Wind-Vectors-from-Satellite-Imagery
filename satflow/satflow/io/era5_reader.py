"""Reader for ERA5 reanalysis data."""

import cdsapi

def read_era5(file_path: str):
    """
    Read ERA5 netCDF or GRIB files and return xarray.Dataset.

    Args:
        file_path (str): Path to ERA5 file

    Returns:
        xarray.Dataset: ERA5 data
    """
    # TODO: Implement reading using xarray and cfgrib
    raise NotImplementedError("ERA5 reader not implemented")
