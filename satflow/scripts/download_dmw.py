"""Download DMW (Deep Motion Winds) datasets."""

import os

def download_dmw(output_dir: str = "../data/raw/dmw"):
    """
    Download DMW data to the raw data directory.

    Args:
        output_dir (str): Path to store downloaded DMW data.
    """
    # TODO: Implement download logic
    os.makedirs(output_dir, exist_ok=True)
    print(f"Downloading DMW data to {output_dir}")

if __name__ == "__main__":
    download_dmw()
