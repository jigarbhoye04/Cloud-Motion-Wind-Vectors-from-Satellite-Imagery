"""Evaluate model predictions against DMW labels."""

import argparse

def evaluate_dmw(pred_dir: str = "../outputs", gt_dir: str = "../data/labels/dmw"):
    """
    Compute DMW metrics for predictions.

    Args:
        pred_dir (str): Prediction directory.
        gt_dir (str): Ground truth DMW labels.
    """
    # TODO: Load predictions and GT, compute metrics
    print(f"Evaluating DMW in {pred_dir} vs {gt_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred', help='Prediction directory')
    parser.add_argument('--gt', help='GT directory')
    args = parser.parse_args()
    evaluate_dmw(args.pred, args.gt)
