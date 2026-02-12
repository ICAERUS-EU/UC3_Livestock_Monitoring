import os
from pathlib import Path
from ultralytics import YOLO
from ultralytics import settings
import torch

# CONFIG
torch.cuda.current_device()

HOME = "your/home/directory"

# update of runs and datasets directories
settings.update({"runs_dir": f"{HOME}/runs"}) 
settings.update({"datasets_dir": f"{HOME}/data"})

# name of your project and run
project = "runs/detect"
run_name = "finetune_all_datasets"

base_weights = "path/to/model/to/finetune"

data_mix = "path/to/data.yaml"

batch = 16


# Phase A: freeze backbone (10 epochs), low LR
epochsA=10
freezeA = 15
lr0_A = 3e-4
lrf_A = 0.1
warmup_epochs_A = 1.0

# Phase B: partial unfreeze, moderate LR, soft scheduler
epochsB = 80
freezeB = 0
lr0_B = 1e-3
lrf_B = 0.01
warmup_epochs_B = 2.0

# data augmentation 
augment_kwargs = dict(
    degrees=0.0,
    translate=0.10,
    scale=0.30,
    shear=0.0,
    perspective=0.0,
    fliplr=0.5,
    flipud=0.0,
    hsv_h=0.015,
    hsv_s=0.5,
    hsv_v=0.4,
    mosaic=0.2,      
    mixup=0.0,       
    copy_paste=0.0
)

# PHASE A: stabilization
model = YOLO(base_weights)

print("\n===== PHASE A (freeze + low LR + replay) =====")
resA = model.train(
data=data_mix,
    epochs=epochsA,
    batch=batch,
    workers = 0,
    project=project,
    name=run_name,
    exist_ok=True,

        freeze=freezeA,
    lr0=lr0_A,
    lrf=lrf_A,
    warmup_epochs=warmup_epochs_A,
    cos_lr=True,

    # stability
    optimizer="SGD",      # more stable in finetuning
    patience=0,           

    # augmentations
    **augment_kwargs,
)

run_dir = Path(resA.save_dir)
bestA = run_dir / "weights" / "best.pt"
lastA = run_dir / "weights" / "last.pt"
weights_for_B = str(bestA if bestA.exists() else lastA)
print(f"\Weights for PHASE B: {weights_for_B}")

# PHASE B: improvement

modelB = YOLO(weights_for_B)

print("\n===== PHASE B (unfreeze + replay + improvements) =====")
resB = modelB.train(
    data=data_mix,
    epochs=epochsB,
    batch=batch,
    workers = 0,
    project=project,
    name=run_name,
    exist_ok=True,

    freeze=freezeB,
    lr0=lr0_B,
    lrf=lrf_B,
    warmup_epochs=warmup_epochs_B,
    cos_lr=True,

    optimizer="SGD",
    patience=25,

    # data augmentation
    **augment_kwargs,
)

print("\nFinish.")
print(f"Run:  {resB.save_dir}")
print(f"Best: {Path(resB.save_dir) / 'weights' / 'best.pt'}")
print(f"Last: {Path(resB.save_dir) / 'weights' / 'last.pt'}")
