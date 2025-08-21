# 🌩️ SatFlow — Cloud Motion & Winds from Geostationary Satellites (Optical Flow + Physics)

SatFlow is a **reproducible, end-to-end system** for estimating **cloud motion** and deriving **winds (u, v, speed, direction)** from **geostationary satellite imagery**. It combines modern **CNN/Transformer optical-flow** models (PWC-Net, RAFT/SEA-RAFT, FlowFormer++), **pseudo-labels** from a teacher model, sparse **DMW** supervision, and light **physics priors** to produce geolocated wind fields in **NetCDF**.

> Use cases: **weather nowcasting (0–6 h)**, **storm tracking**, **situational awareness**, **research**.

---

## 🔑 What you get

- A **production-ready repo** with:
  - Data downloaders for **GOES-16/18** (MCMIPC, ACHA, DMW) and **ERA5**.
  - A robust **preprocessing pipeline** (pairing, tiling, normalization, band selection).
  - **Teacher inference** to generate dense **pseudo-flow** labels.
  - Training for **PWC-Net**, **RAFT/SEA-RAFT**, **FlowFormer++** with **unsupervised + distillation + sparse DMW + physics**.
  - **Evaluation** vs DMW and **ERA5**; **inference** to geolocated NetCDF winds.
- Clear **configs**, **Makefile** commands, **tests**, and **troubleshooting** playbook.

---

## 🧭 Pipeline (Overview)

![Pipeline/Flow](/public/flowchart.png)

```
Raw Satellite Imagery
       |
       v
Preprocessing (channel selection, tiling, normalization)
       |
       v
Label Generation
   ├─ AMV/DMW products (noisy but real labels)
   ├─ Pseudo-labels (from teacher models like RAFT, FlowFormer++)
   └─ ERA5 reanalysis (global, physics-informed fields)
       |
       v
Model Training
   ├─ PWC-Net
   ├─ RAFT
   └─ FlowFormer++
       |
       v
Evaluation
   ├─ Compare against AMV/DMW products
   ├─ Compare against ERA5 wind fields
   └─ Metrics: EPE (endpoint error), angular error, coverage
       |
       v
Outputs
   ├─ NetCDF motion fields
   └─ Visualizations / performance reports

```


---

## 📁 Repository layout

```
satflow/
├─ configs/
│  ├─ goes_conus_10min.yaml                 # AOI, bands, time, levels
│  ├─ training_pwcnet.yaml                  # PWC-Net training cfg
│  ├─ training_raft.yaml                    # RAFT/SEA-RAFT training cfg
│  └─ training_flowformerpp.yaml            # FlowFormer++ training cfg
├─ data/
│  ├─ raw/                                  # netcdf/h5/grib from AWS/CDS
│  ├─ interim/                              # paired indices, tiles
│  └─ labels/                               # DMW, pseudo-flows, ERA5 samples
├─ satflow/
│  ├─ io/                                   # GOES/ACHA/DMW/ERA5 readers
│  ├─ geo/                                  # geodesy, meters-per-pixel
│  ├─ prep/                                 # pairing, tiling, normalization
│  ├─ teachers/                             # RAFT/FlowFormer teacher inference
│  ├─ models/                               # PWCNet, RAFT wrapper, FlowFormer++
│  ├─ losses/                               # photo, census, smooth, fb, div, sparse
│  ├─ physics/                              # height-aware mapping, continuity priors
│  ├─ train/                                # loops, schedulers, AMP, ckpt
│  ├─ eval/                                 # metrics vs DMW/ERA5, EPE, AE
│  └─ infer/                                # tiling, stitching, NetCDF writer
├─ scripts/
│  ├─ download_goes.py
│  ├─ download_dmw.py
│  ├─ download_era5.py
│  ├─ make_pairs.py
│  ├─ make_pseudo_labels.py
│  ├─ collocate_dmw.py
│  ├─ train.py
│  ├─ eval_dmw.py
│  └─ infer_tiles.py
├─ environment.yml
├─ Makefile
└─ README.md
```

---

## 🛰️ Data sources (what & why)

* **GOES-16/18 ABI L2 MCMIPC** (Cloud & Moisture Composite Imagery): multi-spectral inputs (**WV 8–10**, **IR 13**, **VIS 2** by day).
* **GOES ABI L2 ACHA / CTP**: Cloud-Top Height/Pressure per pixel → maps image motion to a **height level** for winds.
* **GOES ABI L2 DMW** (Derived Motion Winds): **sparse “ground-truth-like”** wind vectors (lat, lon, speed, dir, pressure, QC).
* **ERA5** reanalysis (pressure-level u, v): coarse but **physically consistent** winds → **weak prior/sanity**.

**Sectors & cadence**:

* **FD** (\~10 min), **CONUS** (\~5–10 min), **MESO** (as fast as 1–5 min).
* Choose **Δt** (5/10/15 min) that matches sector/cadence for stable training.

---

## 🧩 Concepts (plain English, deeply explained)

### Optical Flow (dense motion)

* Predicts a **vector (du, dv)** at **every pixel** describing motion from time `t` to `t+Δt`.
* Convert pixel displacement to **meters/second** using **meters per pixel** and **Δt**.

### Bands (which channels matter?)

* **WV (8, 9, 10)**: water vapor → strong mid/upper-troposphere cloud motion signal.
* **IR window (13)**: cloud-top temp texture both **day & night**.
* **VIS (2)**: great texture **by day**, unavailable at night (omit or gate).

### DMW (Derived Motion Winds)

* Agency product that *tracks* “features” (cloud/tracer) to produce **sparse winds** with QC and pressure level.
* Use for **evaluation** and **sparse supervision** (not absolute truth; treat as **anchor**).

### ERA5 (reanalysis)

* Coarse grid, globally consistent physics. Use **softly**: sanity check, gentle priors.

### Teacher / Pseudo-labels

* A strong pre-trained flow model (**RAFT/SEA-RAFT**) run on your pairs → **dense pseudo-flow**.
* Student models learn by **distillation** (match teacher where confident).

### Physics priors (light & helpful)

* **Continuity / low divergence**: clouds approximately conserve mass at scale → penalize `∇·u`.
* **Height-aware**: compare to DMW/ERA5 at **ACHA-implied pressure** (e.g., ±50 hPa).

### Models (how they differ)

* **PWC-Net**: pyramid + warping + local cost volumes → **fast/light** baseline.
* **RAFT / SEA-RAFT**: **all-pairs correlation** + recurrent updates → **accurate**, more memory.
* **FlowFormer++**: **Transformer** over tokenized 4D cost → **global context**, best on complex flows, heavier.

### Metrics (what “good” looks like)

* **EPE** (End-Point Error): √((Δu)²+(Δv)²) — dense (vs teacher) or sparse (vs DMW sample).
* **Angular error (deg)**: misalignment of predicted vs DMW vectors.
* **Vector RMSE** and **Speed RMSE**: magnitude and component errors.
* Stratify by **pressure levels**, **QC**, **day/night**.

---

## 🔧 Setup

### Requirements

* **GPU**: ≥12 GB (RAFT @ 512px tiles). For FlowFormer++, 24 GB recommended (use grad-accum if less).
* **OS**: Linux / WSL2 / macOS (training on CPU not recommended).
* **Conda**: Miniconda/Anaconda.

### Install

```bash
# Create env
conda env create -f environment.yml
conda activate satflow

# (Windows/WSL) public S3 buckets w/o creds
# PowerShell:
setx AWS_NO_SIGN_REQUEST 1
# bash:
export AWS_NO_SIGN_REQUEST=1
```

---

## ⚙️ Configure your run

`configs/goes_conus_10min.yaml` (example)

```yaml
region: [-125.0, 23.0, -66.0, 50.0]   # lon_min, lat_min, lon_max, lat_max (CONUS)
dataset:
  satellite: noaa-goes16
  products: [ABI-L2-MCMIPC, ABI-L2-ACHA, ABI-L2-DMWC]
  cadence_minutes: 10
  bands: [8,9,10,13]                  # WVx3 + IR window
time:
  start: "2024-09-01T18:00:00Z"
  end:   "2024-09-01T23:59:59Z"
era5:
  pressure_levels: [950, 850, 700, 500, 400, 300, 250]
  variables: [u, v, t, q]
```

---

## 🚀 Quickstart (10 commands)

```bash
# 1) env
conda env create -f environment.yml && conda activate satflow

# 2) init (installs, sanity checks)
make init

# 3) pull GOES (MCMIPC/ACHA/DMW) within config time window
make pull-goes

# 4) build training pairs (Δt = 10 min), write parquet index
make pairs

# 5) generate pseudo-flows with RAFT teacher
make pseudo

# 6) collocate sparse DMW (optional but recommended)
python scripts/collocate_dmw.py --config configs/goes_conus_10min.yaml \
  --pairs-file data/interim/pairs_10min.parq --out data/labels/dmw_collocated.parq

# 7) train baseline (PWC-Net) – unsupervised warmup
make train-pwc

# 8) train RAFT – add distillation (+ DMW + physics in later stage)
make train-raft

# 9) evaluate vs DMW (pressure-stratified)
make eval

# 10) inference → NetCDF winds
make infer
```

---

## 🛠️ Scripts & CLIs

### Data acquisition

```bash
# GOES imagery + ACHA + DMW from public AWS (no credentials)
python scripts/download_goes.py --config configs/goes_conus_10min.yaml --no-sign-request
# ERA5 pressure-level winds (requires CDS API key)
python scripts/download_era5.py --config configs/goes_conus_10min.yaml
```

### Preprocessing

```bash
# Build (I_t, I_{t+Δt}) pairs; tile and normalize (config-driven)
python scripts/make_pairs.py --config configs/goes_conus_10min.yaml
```

### Pseudo-labels (teacher)

```bash
python scripts/make_pseudo_labels.py \
  --pairs-file data/interim/pairs_10min.parq \
  --teacher raft --ckpt external/raft/raft-things.pth \
  --bands 8 9 10 13 --tile 512 --stride 256 \
  --out data/labels/pseudo/raft_10min
```

### Training (stages)

```bash
# Stage-1: Unsupervised warm-up (PWC-Net)
python scripts/train.py --config configs/training_pwcnet.yaml \
  TRAIN.losses="[photo,census,smooth,fb]" TRAIN.epochs=20

# Stage-2: Distillation (RAFT/SEA-RAFT)
python scripts/train.py --config configs/training_raft.yaml \
  TRAIN.losses="[photo,smooth,fb,distill]" TRAIN.w_distill=1.0

# Stage-3: + Sparse DMW + Physics
python scripts/train.py --config configs/training_raft.yaml \
  TRAIN.losses="[photo,smooth,fb,distill,dmw,div,era]" \
  TRAIN.w_dmw=0.5 TRAIN.w_div=0.2 TRAIN.w_era=0.2 DATA.dmw_qc_min=0.7

# Stage-4: FlowFormer++ (reduce batch; use grad accumulation)
python scripts/train.py --config configs/training_flowformerpp.yaml TRAIN.grad_accum=4
```

### Evaluation & Inference

```bash
# Evaluate predictions against DMW (RMSE, angular, level bins)
python scripts/eval_dmw.py --pred data/pred/raft_uv_10min/ \
  --dmw data/labels/dmw_collocated.parq --out reports/dmw_eval.csv

# Tiled inference → NetCDF with u, v, speed, dir, lat, lon, time, height
python scripts/infer_tiles.py \
  --model checkpoints/raft_satcloud.pt \
  --pairs-file data/interim/pairs_10min.parq \
  --tile 768 --stride 512 --bands 8 9 10 13 \
  --accha-dir data/raw/goes16/ACHA/ --write-nc True \
  --out data/pred/raft_uv_10min/
```

---

## 🧮 From pixel flow to winds (u, v in m/s)

Given pixel displacement **(du, dv)** over **Δt** and local **meters-per-pixel** (**mx, my**):

* **Δx\_m = du · mx**, **Δy\_m = dv · my**
* **u = Δx\_m / Δt**, **v = Δy\_m / Δt**
  Meters-per-degree varies with latitude (lon scaling \~ `cos(lat)`); use `pyproj/Geod` or a local tangent-plane approximation.
  Attach **pressure/height** from **ACHA** to align with DMW/ERA5 (e.g., within ±50 hPa).

---

## 📊 Metrics (formulas)

* **Vector RMSE**:
  `RMSE = sqrt( mean( (û - u)² + (v̂ - v)² ) )`
* **Speed RMSE**:
  `RMSE_speed = sqrt( mean( (|V̂| - |V|)² ) )`
* **Angular error (deg)**:
  `θ = arccos( (ûu + v̂v) / (|V̂||V| + ε) ) · 180/π`
* **EPE (dense vs teacher)**: L2 per-pixel, averaged.

Stratify by **pressure bins** (e.g., 950–850, 850–700, ...), **QC** (≥0.7), **day/night**.

---

## 🧪 Training stages (why staged?)

1. **S1 Unsupervised**: learn photometric alignment (multi-band) + smooth flow; ignore occlusions.
2. **S2 Distillation**: bring student closer to strong teacher (RAFT/SEA-RAFT).
3. **S3 Sparse DMW + Physics**: add trustworthy sparse anchors + weak continuity prior.
4. **S4 FlowFormer++**: step up model capacity with careful memory management.

> Keep **photometric loss non-zero** to remain image-faithful; ramp **distillation then DMW**.

---

## 🧱 Practical defaults & hardware notes

* **Tiles**: 512–768 px, **stride** 256–512, **overlap** \~128 px for inference stitching.
* **Memory**: RAFT \~10–14 GB @ 512–640 tiles; use **AMP**, **grad accumulation**, smaller tiles.
* **Bands**: At night, drop VIS (#2). Prefer **WV (8–10) + IR (13)**.
* **Δt**: 10 min is robust; **5 min MESO** gives sharper vectors but higher compute.

---

## 🧰 Makefile targets

```
init           # env setup (environment.yml), sanity checks
pull-goes      # download GOES MCMIPC/ACHA/DMW per config
pairs          # build pair index + (optional) tiles
pseudo         # teacher inference → pseudo-flow labels
train-pwc      # train PWC-Net (warm-up)
train-raft     # train RAFT/SEA-RAFT (distill, dmw, physics)
train-flowformer
eval           # DMW/ERA5 metrics, reports
infer          # tiled inference → NetCDF winds
```

---

## 🔬 Reproducibility & experiment tracking

* **Seeds**: torch/cuDNN seeded where feasible (deterministic ops toggled).
* **Configs**: versioned under `configs/`; CLI can override keys.
* **Logs**: TensorBoard scalars & images; optional W\&B if `WANDB_API_KEY` set.
* **Sweeps**: `scripts/sweep.py` to grid search loss weights & band sets.
* **Run cards**: auto-filled markdown summaries in `reports/`.

---

## 🧯 Troubleshooting playbook

* **CUDA OOM at 768px tiles on 12 GB**
  → Enable AMP, reduce tile to 512, increase stride, set `TRAIN.grad_accum=4`, enable gradient checkpointing (FlowFormer++). Resume from last checkpoint via `TRAIN.resume=...`.

* **Noisy night flows on WV**
  → Downweight WV in photometric loss, add a texture mask (downweight low gradients), add temporal smoothness prior; verify normalization stats by band.

* **High angular error vs DMW at 300 hPa**
  → Pressure-aware sampling (ACHA pressure ±50 hPa), increase `w_dmw` with a curriculum, inspect collocation tolerances & QC.

* **Domain shift (CONUS → tropics/MESO)**
  → Re-normalize distributions (per-band robust z-scores), histogram matching, increase tile overlap, adapt Δt to sector cadence.

---

## 🧾 Output (NetCDF) schema

Per pair `(t, t+Δt)` one file with:

* Variables: `u`, `v` (m/s), `speed`, `dir`, `lat`, `lon`, `p` (optional pressure/Pa), `height` (m).
* Attributes: `time_start`, `time_end`, `delta_t`, `model`, `bands`, `projection`, `source_paths`, `git_commit`, `training_config`.

Example names:
`data/pred/raft_uv_10min/2024-09-01T18:10Z_conus_u-v.nc`

---

## ❓ FAQ (short)

* **Is DMW ground truth?**
  It’s a high-quality **algorithmic** product (sparse, QC’d). Use as **anchor**, not absolute truth.

* **Why ERA5 then?**
  ERA5 gives **physics-consistent** coarse winds. Use for **soft** guidance/sanity—don’t force exact match.

* **Single-band training possible?**
  Yes, but multi-band (WV + IR) is more robust, especially at night.

* **Why FlowFormer++?**
  Global attention over tokenized 4D cost handles large/complex motions better; heavier memory.

---

## 👥 Contributing

* Run unit tests (`pytest -q`) before PRs.
* Keep modules **pure & testable**; prefer **config-driven** over hardcoded values.
* Add docstrings, examples, and **small fixtures** for new readers/prep steps.

---

## 🔗 Pointers (non-exhaustive)

* Optical Flow: **PWC-Net**, **RAFT**, **SEA-RAFT**, **FlowFormer++**
* Satellite products: **GOES ABI L2** (MCMIPC, ACHA/CTP, DMW)
* Reanalysis: **ERA5** (ECMWF)
* Geodesy: `pyproj`, `rioxarray`, `xarray`

---

Our final outcome is a fully functional, modular pipeline that turns raw satellite cloud imagery into physically consistent motion vectors (AMVs). These vectors outperform traditional methods in density and accuracy, and are directly usable in weather forecasting and climate science. Beyond the models, the project produces reusable datasets, trained networks, and evaluation benchmarks — essentially a toolkit for next-gen satellite motion vector research.

## ✅ Readiness checklist

* [ ] `conda activate satflow` works; `python -c "import torch,xarray"` passes.
* [ ] `make pull-goes` pulls at least a few scenes.
* [ ] `data/interim/pairs_10min.parq` exists with >0 rows.
* [ ] Pseudo-labels generated (`data/labels/pseudo/...` present).
* [ ] Training produces checkpoints; TensorBoard losses trend down.
* [ ] `make eval` yields sane metrics; quiver overlays look aligned.
* [ ] Inference NetCDF contains u/v/speed/dir with geolocation & attrs.
