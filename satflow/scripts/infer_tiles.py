"""Inference script to process tiles and write NetCDF."""

import argparse

def infer_tiles(input_dir: str = "../data/raw/goes", out_dir: str = "../outputs/infer"):
    """
    Run inference on raw GOES data tiles and save NetCDF.

    Args:
        input_dir (str): Directory with raw GOES tiles
        out_dir (str): Output NetCDF directory
    """
    # TODO: Implement inference pipeline
    print(f"Inferring tiles from {input_dir} to {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input tile directory')
    parser.add_argument('--out', help='Output directory')
    args = parser.parse_args()
    infer_tiles(args.input, args.out)
