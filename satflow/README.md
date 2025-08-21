# SatFlow

SatFlow is a pipeline for satellite cloud-motion optical flow estimation. It uses deep learning to estimate motion vectors from geostationary satellite imagery and can leverage pseudo-labels, teacher models (RAFT, FlowFormer++), and physical constraints.

## Data Sources

- GOES-16/18 L2 MCMIPC, ACHA, DMW (AWS, NOAA)
- ERA5 (ECMWF)

## Pipeline Diagram

```
Raw Data
   |
   v
Preprocessing (pairing, tiling, normalization)
   |
   v
Label Generation (DMW, pseudo-flows, ERA5)
   |
   v
Model Training (PWC-Net, RAFT, FlowFormer++)
   |
   v
Evaluation & Inference
   |
   v
Outputs (NetCDF, metrics)
``` 

## Quickstart

```bash
# 1. Create environment and install dependencies
conda env create -f environment.yml
conda activate satflow

# 2. Initialize repository (download data, configs)
make init

# 3. Train a baseline model
make train-pwc

# 4. Evaluate
make eval

# 5. Inference
make infer
```

## Commands

- `make init`       : Set up data folders and download default data samples
- `make pull-goes`  : Download GOES imagery samples
- `make pairs`      : Generate paired tensors for training
- `make pseudo`     : Create pseudo-labels using teacher models
- `make train-pwc`  : Train PWC-Net model
- `make train-raft` : Train RAFT model
- `make train-flowformer` : Train FlowFormer++ model
- `make eval`       : Evaluate on DMW and ERA5 metrics
- `make infer`      : Run inference on tile grid and save NetCDF
