# Script to organize GOES AMV GIF files into folders based on their timestamp.


import os
import shutil
from pathlib import Path

# === CONFIGURATION ===
source_dir = "Datasets/GOES/data9PHk0e"     # Folder containing all the GIFs
target_dir = "Datasets/GOES/organized"  # Where you want organized folders

# === CREATE TARGET ROOT FOLDER IF NEEDED ===
os.makedirs(target_dir, exist_ok=True)

# === PROCESS ALL FILES ===
for filename in os.listdir(source_dir):
    if filename.endswith(".gif") and filename.startswith("ops.GOES_AMV"):
        # Split the filename
        parts = filename.split(".")
        if len(parts) >= 4:
            timestamp = parts[2]                # e.g., 201106141500
            variable = ".".join(parts[3:])      # everything after the timestamp

            # Create the timestamp folder
            timestamp_folder = os.path.join(target_dir, timestamp)
            os.makedirs(timestamp_folder, exist_ok=True)

            # Copy (or move) the file into that folder
            src_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(timestamp_folder, variable)
            shutil.copy2(src_path, dest_path)  # use shutil.move() to move instead

print("✅ Dataset organized successfully by timestamp.")
