"""Train optical flow models based on configs."""

import argparse
import yaml


def train_model(config_path: str):
    """
    Train selected optical flow model based on YAML config.

    Args:
        config_path (str): Path to training YAML
    """
    # TODO: Implement model initialization and training loop
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    print(f"Training {cfg['model']} with config {config_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Path to config YAML')
    args = parser.parse_args()
    train_model(args.config)
