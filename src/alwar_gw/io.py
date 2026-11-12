"""Reading and writing the block-daily tables, and saving safely to Drive."""
import os
import shutil

import pandas as pd

META_COLS = ("Date", "Year", "Month", "Day")


def read_blocks(path):
    """Read a ``*_AlwarBlocks.csv`` file → DataFrame indexed by Date, one column per block."""
    df = pd.read_csv(path, parse_dates=["Date"]).set_index("Date")
    return df.drop(columns=[c for c in ("Year", "Month", "Day") if c in df.columns])


def write_blocks(df, path):
    """Write a Date-indexed block table in the standard layout (Date, Year, Month, Day, blocks…)."""
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    out = df.copy()
    out.insert(0, "Day", out.index.day)
    out.insert(0, "Month", out.index.month)
    out.insert(0, "Year", out.index.year)
    out.index.name = "Date"
    tmp = str(path) + ".tmp"
    out.reset_index().to_csv(tmp, index=False)
    os.replace(tmp, path)


def block_columns(df):
    """Names of the block columns (they start with the 3-digit LGD code, e.g. ``574_BANSUR``)."""
    return [c for c in df.columns if str(c)[:3].isdigit()]


def save_via_local(write_func, drive_path, tmp_dir="/content/_tmp_save"):
    """Write a file on Colab's local disk, then copy it to Drive.

    Use this for SQLite-based formats (GeoPackage ``.gpkg``): writing them straight
    onto the Drive mount can fail silently.

        save_via_local(lambda p: gdf.to_file(p, driver="GPKG"), f"{GRID}/cells.gpkg")
    """
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(os.path.dirname(str(drive_path)), exist_ok=True)
    local = os.path.join(tmp_dir, os.path.basename(str(drive_path)))
    write_func(local)
    shutil.copy2(local, drive_path)
    return drive_path
