"""Generate paired training samples from raw data."""

import os

def make_pairs(raw_dir: str = "../data/raw", out_dir: str = "../data/interim/pairs"):
    """
    Create paired image tensors for optical flow training.

    Args:
        raw_dir (str): Directory with raw imagery
        out_dir (str): Directory for paired output
    """
    os.makedirs(out_dir, exist_ok=True)
    # TODO: Implement pairing logic
    print(f"Creating pairs in {out_dir}")

if __name__ == "__main__":
    make_pairs()
