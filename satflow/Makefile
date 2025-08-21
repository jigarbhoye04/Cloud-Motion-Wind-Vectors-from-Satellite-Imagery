.PHONY: init pull-goes pairs pseudo train-pwc train-raft train-flowformer eval infer

init:
	python scripts/download_goes.py && python scripts/download_dmw.py && python scripts/download_era5.py

pull-goes:
	python scripts/download_goes.py

pairs:
	python scripts/make_pairs.py

pseudo:
	python scripts/make_pseudo_labels.py

train-pwc:
	python scripts/train.py --config configs/training_pwcnet.yaml

train-raft:
	python scripts/train.py --config configs/training_raft.yaml

train-flowformer:
	python scripts/train.py --config configs/training_flowformerpp.yaml

eval:
	python scripts/eval_dmw.py

infer:
	python scripts/infer_tiles.py
