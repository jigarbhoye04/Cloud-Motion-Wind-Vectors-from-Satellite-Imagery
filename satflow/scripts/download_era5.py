"""Download ERA5 reanalysis samples using CDSAPI."""

import os
import cdsapi

def download_era5(output_dir: str = "../data/raw/era5"):
    """
    Download ERA5 samples to the raw data directory.

    Args:
        output_dir (str): Path to store downloaded ERA5 data.
    """
    os.makedirs(output_dir, exist_ok=True)
    c = cdsapi.Client()
    # TODO: Define variables, date ranges in request
    print(f"Requesting ERA5 data to {output_dir}")

if __name__ == "__main__":
    download_era5()
