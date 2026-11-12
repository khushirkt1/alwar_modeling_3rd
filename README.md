# Alwar groundwater model

Modelling the effect of climate change and human use on groundwater in **Alwar, Rajasthan** (14 blocks, LGD 574–587, about 7,800 km²).

The workflow runs in **Google Colab**. Code lives in this repository; **all data stay on Google Drive** under `MyDrive/gw_framework/` and are never committed.

```
observed data ──► cleaning, QC, trends ─┐
climate (IMD, CMIP6) ──► block forcing ─┼─► recharge ─► MODFLOW 6 ─► calibration ─► scenarios
boreholes, maps, GEC ──► aquifer zones ─┘
```

## Quick start

1. Put this repository on GitHub — step by step in [`docs/GITHUB_AND_COLAB.md`](docs/GITHUB_AND_COLAB.md).
2. In Colab: **File → Open notebook → GitHub**, choose this repository and a notebook.
3. Run the first cell (**SETUP**). The first time, it asks for `username/repo-name` and remembers it on your Drive. It mounts Drive, fetches this repository into Colab, and installs any missing packages.
4. Run the remaining cells from top to bottom.

Direct link pattern for any notebook:
`https://colab.research.google.com/github/<username>/<repo>/blob/main/notebooks/<folder>/<notebook>.ipynb`

## Repository layout

```
├── README.md
├── requirements.txt
├── src/alwar_gw/            shared helpers (Drive paths, Colab set-up, block-table I/O)
├── notebooks/
│   ├── 01_data/             inventory, station rainfall, groundwater levels, domain and trends
│   ├── 02_climate/          CMIP6 and IMD forcing for the 14 blocks
│   ├── 03_hydrogeology/     boreholes, lithology, geology maps, GEC, aquifer zones, DEM
│   ├── 04_model/            MODFLOW 6 grid and models
│   └── 99_archive/          superseded cells, kept for reference
└── docs/                    methods, data locations, status, cell index
```

## Notebooks

Status: ✅ done · 🟡 in progress, or outputs were not saved in the source notebook so completion can't be confirmed from it · ⚠️ superseded (kept as a record) · 🧪 test only

| # | Notebook | What it does | Status |
|---|---|---|---|
| **01_data** | | | |
| 1 | `01_data_inventory` | What is on Drive: NetCDF, tables, rasters, shapefiles | ✅ |
| 2 | `02_station_rainfall_PDFs` | Daily station rainfall 2010–2025 from the Rajasthan PDFs | ✅ |
| 3 | `03_groundwater_levels_cleaning_QC` | 13 district Excel files → cleaned seasonal water levels; Alwar source recovery | ✅ |
| 4 | `04_study_domain_and_gw_trends` | 14-block domain; Mann–Kendall/Sen/TFPW trends; maps and clusters | ✅ |
| **02_climate** | | | |
| 5 | `01_cmip6_extraction_v1_SUPERSEDED` | First CMIP6 extraction (block weights are still used) | ⚠️ |
| 6 | `02_cmip6_temperature_QC_v1_SUPERSEDED` | Tmax < Tmin and −273.15 °C investigation on the first extraction | ⚠️ |
| 7 | **`03_climate_forcing_corrected`** | **IMD + 13 GCMs × 5 scenarios, cleaned, monthly QDM, PET — the forcing to use** | ✅ |
| **03_hydrogeology** | | | |
| 8 | `01_BDR_PDF_screening_and_CGWB` | BDR PDF screening, OCR, CGWB parameter search | ✅ (nothing verified from PDFs) |
| 9 | `02_BDR_lithology_database` | Borehole database from the Atal/NHP Word files: coordinates, lithology review, elevations | 🟡 |
| 10 | `03_hydrostratigraphy_correlation_sections` | Hydrostratigraphic groups, correlation screening, preliminary sections | 🟡 |
| 11 | `04_geology_GSI_plate_georeferencing` | Georeferencing the GSI geological map (Plate IV) | 🟡 |
| 12 | `05_geology_NATMO_GSI_crosswalk` | NATMO/GSI map evidence and borehole crosswalk | 🟡 |
| 13 | `06_gec_aquifer_zones_dem` | GEC 2024-25 per block, aquifer class of 474 wells, 30 m DEM | ✅ |
| **04_model** | | | |
| 14 | `01_modflow_first_pass_synthetic` | MODFLOW 6 test on a synthetic 20 × 20 grid | 🧪 |
| 15 | `02_transient_obs_preparation` | Observation table and well database for the transient model | 🟡 |
| 16 | `03_grid_and_steady_state` | 1 km Alwar grid and steady-state plumbing check | 🟡 (run and review) |
| **99_archive** | `archive_superseded_cells` | 79 cells that failed, were duplicated, or only searched Drive | — |

`docs/cell_index.csv` lists where each of the 367 cells of the original working notebook (`alwargwd_data_analysis_2_2.ipynb`) went.

## Important: which climate files to use

The first CMIP6 extraction (notebooks 5 and 6) read grid columns at `3 + column_index_zero_based`. The index already counts the three date columns, so those cells are about 0.75° **north of Alwar**. Everything under `Alwar_daily_extracted*`, `Alwar_block_daily_forcing*` and `*_REBUILT` on Drive comes from the wrong cells.

Use only the outputs of `02_climate/03_climate_forcing_corrected.ipynb`:

`gw_framework/inputs/alwar/climate_cmip6_qdm/<scenario>/<model>_<scenario>_<variable>_AlwarBlocks.csv`

Details: [`docs/CLIMATE_FORCING_methods.md`](docs/CLIMATE_FORCING_methods.md).

## How the notebooks are built

- **Notebooks 1–6, 8–12, 14–15** hold the cells of the original working notebook, **unchanged**, grouped by stage with headings and a label on every cell (`[orig #N]` and how its last run ended). Outputs are cleared. Their paths are hard-coded to `MyDrive/gw_framework/`.
- **Notebooks 7, 13 and 16** are the validated pipeline written afterwards. Their computing code is the code that ran successfully in Colab; a few read-only diagnostic print-outs were shortened and cells were merged, and they have not been rerun in this exact form.
- Every notebook starts with the same **SETUP** cell.
- Notebooks pass data to each other **only through files on Drive**, so each one can run in a fresh Colab session.

## Rules for adding work

1. One notebook = one stage = one output folder. Split a notebook when it passes about 40 code cells.
2. Fix a cell in place; don't add a "fix" cell below it.
3. Don't print whole tables: `display(df.head())`, and save the full table to CSV.
4. **Edit → Clear all outputs** before saving to GitHub.
5. Model-ready files go to `gw_framework/inputs/alwar/`; take paths from `alwar_gw.paths`.
6. Write GeoPackage (`.gpkg`) files to `/content` first and copy them to Drive (`alwar_gw.io.save_via_local`), or use Parquet.

## Documentation

| File | Contents |
|---|---|
| [`docs/GITHUB_AND_COLAB.md`](docs/GITHUB_AND_COLAB.md) | Uploading to GitHub, opening in Colab, private repositories, saving changes, troubleshooting |
| [`docs/WORKFLOW_AND_STATUS.md`](docs/WORKFLOW_AND_STATUS.md) | Run order, key results so far, next steps |
| [`docs/CLIMATE_FORCING_methods.md`](docs/CLIMATE_FORCING_methods.md) | Climate methods and numbers for the thesis |
| [`docs/DATA_ON_DRIVE.md`](docs/DATA_ON_DRIVE.md) | Where every input and output lives on Drive |
| [`docs/DATA_LINEAGE_GAPS.md`](docs/DATA_LINEAGE_GAPS.md) | Files the notebooks read but no notebook creates |
| `docs/cell_index.csv` | Original cell → notebook, section, last-run status |

## Data sources

IMD gridded rainfall (Pai et al. 2014) and temperature; Mishra et al. (2020) bias-corrected CMIP6 projections for South Asia; Rajasthan Ground Water Department well records and BDR reports (Atal Bhujal Yojana, NHP); CGWB / GEC dynamic groundwater resource assessment 2024-25; GSI and NATMO maps; Copernicus GLO-30 DEM; LGD block boundaries. Check each source's terms before redistributing data.

## Licence

No licence file is included yet. Add one (for example MIT for the code) before making the repository public if you want others to reuse it.
