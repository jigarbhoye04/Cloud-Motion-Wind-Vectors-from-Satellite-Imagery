"""Download GOES imagery samples from AWS."""

import os


def download_goes(output_dir: str = "../data/raw/goes"):
    """
    Download GOES-16/18 L2 data to the raw data directory.

    Args:
        output_dir (str): Path to store downloaded GOES data.
    """
    # TODO: Implement AWS S3 download logic using s3fs or boto3
    os.makedirs(output_dir, exist_ok=True)
    print(f"Downloading GOES data to {output_dir}")


if __name__ == "__main__":
    download_goes()
