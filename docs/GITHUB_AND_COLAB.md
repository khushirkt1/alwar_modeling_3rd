# Putting the project on GitHub and running it in Colab

## 1. Create the repository (once)

1. Sign in at <https://github.com> → **+** (top right) → **New repository**.
2. Name it, for example `alwar-groundwater-model`. Choose **Public** or **Private**.
3. Leave "Add a README", ".gitignore" and "licence" **unticked** (the zip already has them) → **Create repository**.

## 2. Upload the files (once)

1. Unzip `alwar-groundwater-model.zip` on your computer.
2. On the new repository page click **uploading an existing file**.
3. Open the unzipped folder, select **everything inside it** (`README.md`, `requirements.txt`, `.gitignore`, `notebooks`, `src`, `docs`) and drag it onto the page. Use Chrome or Edge so that folders upload with their structure.
4. Wait for the upload to finish → **Commit changes**.

`.gitignore` is a hidden file on macOS/Linux. If you can't see it, skip it — it only stops data files being committed by accident.

Check: the repository's first page should show `README.md` rendered, and the folders `notebooks/`, `src/`, `docs/`.

## 3. Open a notebook in Colab

1. Go to <https://colab.research.google.com> → **File → Open notebook → GitHub**.
2. Type your GitHub username, pick the repository, pick a notebook.
   For a private repository tick **Include private repos** and authorise Colab.
3. Run the first cell, **SETUP**:
   - it mounts Google Drive;
   - the **first time only**, it asks: `GitHub repository (username/repo-name):` — type for example `yourname/alwar-groundwater-model`. The answer is saved in `MyDrive/gw_framework/repo_config.json`, so no notebook asks again;
   - it downloads the repository to `/content/<repo-name>` (or updates it) and installs missing packages.
4. Run the other cells in order.

### Private repository: one extra step

The SETUP cell has to download `src/` from GitHub. For a private repository give it a token:

1. GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**. Repository access: only this repository. Permissions: **Contents → Read-only**. Copy the token.
2. In Colab click the **key icon** (Secrets) in the left bar → **Add new secret** → name `GH_TOKEN`, value = the token → switch on **Notebook access**.

The token stays in your Colab account; it is never written into a notebook.

## 4. Saving your changes back to GitHub

A notebook opened from GitHub is a temporary copy. To keep changes:

1. **Edit → Clear all outputs** (keeps the repository small; an output-heavy notebook is what made the original 14 MB).
2. **File → Save a copy in GitHub** → choose the repository and the same file path → add a short message → OK.

To change `src/alwar_gw/*.py`, edit the file on GitHub (pencil icon) and commit; the next SETUP run pulls the new version.

## 5. Troubleshooting

| Message | Cause | Fix |
|---|---|---|
| `Mountpoint must not already contain files` | After a restart a cell created folders at `/content/drive` before Drive was mounted | Run the cell below, then SETUP again |
| `Could not clone '<name>'` | Wrong `username/repo-name`, or a private repository without `GH_TOKEN` | The saved name is removed automatically; run SETUP again and type the correct name (add the `GH_TOKEN` secret if private) |
| `ModuleNotFoundError: alwar_gw` | SETUP was not run in this session | Run the SETUP cell |
| `FileNotFoundError` on a Drive path | The notebook that creates that file has not been run, or the file was made outside the notebooks | See `docs/WORKFLOW_AND_STATUS.md` (run order) and `docs/DATA_LINEAGE_GAPS.md` |
| A `.gpkg` file is missing although the cell printed "Saved" | SQLite files don't write reliably onto the Drive mount | Write to `/content` first and copy (`alwar_gw.io.save_via_local`), or save Parquet |
| Thousands of `DeprecationWarning: datetime.utcnow()` lines | A Colab/jupyter message | SETUP hides it; if it returns, run SETUP again |

Cell for the mount problem (removes only **empty** local folders; it refuses to delete files):

```python
import os
MP = "/content/drive"
if not os.path.ismount(MP):
    files = [os.path.join(r, f) for r, _, fs in os.walk(MP) for f in fs]
    assert not files, f"Local files found, move them first: {files[:5]}"
    for root, dirs, _ in os.walk(MP, topdown=False):
        for d in dirs:
            os.rmdir(os.path.join(root, d))
    from google.colab import drive
    drive.mount(MP)
print("Mounted:", os.path.ismount(MP))
```

## 6. Using the helpers in new cells

```python
from alwar_gw import paths as P, io

P.check()                                             # which key inputs exist on Drive
rain = io.read_blocks(P.CLIMATE_OBS / "IMD_rain_AlwarBlocks.csv")
pr = io.read_blocks(P.cmip6_file("EC-Earth3", "ssp245", "PrecipData"))   # QDM forcing
io.write_blocks(pr.resample("MS").sum(), P.ALWAR / "tmp" / "EC-Earth3_ssp245_monthly.csv")
```
