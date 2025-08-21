"""Generate pseudo-labels using teacher models."""

import os

def make_pseudo_labels(pairs_dir: str = "../data/interim/pairs", out_dir: str = "../data/labels/pseudo"):
    """
    Use RAFT or FlowFormer++ teacher models to generate pseudo optical flow labels.

    Args:
        pairs_dir (str): Paired input tensors
        out_dir (str): Output pseudo-labels directory
    """
    os.makedirs(out_dir, exist_ok=True)
    # TODO: Load teacher models and inference
    print(f"Creating pseudo labels in {out_dir}")

if __name__ == "__main__":
    make_pseudo_labels()
