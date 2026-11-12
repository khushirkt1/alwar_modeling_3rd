# Where the data live on Google Drive

Root: `/content/drive/MyDrive/gw_framework` (written `GW/` below). The same paths are available in code as `alwar_gw.paths`.
Nothing in this list is stored in the GitHub repository.

## Model-ready inputs — `GW/inputs/alwar/` (the hand-off folder)

| Path | Contents | Made by |
|---|---|---|
| `blocks.geojson`, `domain.geojson` | 14 blocks (EPSG:4326; `block_lgd`, `block_name`, `district`) and their union. Bounds 76.114–77.211 E, 27.055–28.222 N | `02_climate/03` |
| `climate_obs/IMD_{rain,tmax,tmin,pet_hs}_AlwarBlocks.csv` | IMD per block; rain 1951–2025, temperature and PET 1980–2024 | `02_climate/03` |
| `climate_cmip6/<scenario>/…_AlwarBlocks.csv` | CMIP6 per block, dataset bias correction + cleaning | `02_climate/03` |
| **`climate_cmip6_qdm/<scenario>/…_AlwarBlocks.csv`** | **final forcing** (monthly QDM, wet-day adaptation, PET) | `02_climate/03` |
| `gec/gec_2024_25_alwar_flat.csv`, `gec_2024_25_blocks.csv`, `gec_vs_trends_implied_Sy.csv` | GEC 2024-25 per block in mm and m³/day; implied specific yield | `03_hydrogeology/06` |
| `aquifer/wells_formation_classified.csv`, `block_terrain_summary.csv` | 474 wells with aquifer class and bedrock type; terrain per block | `03_hydrogeology/06` |
| `dem_alwar_utm43n_30m.tif`, `slope_alwar_deg.tif` | Copernicus GLO-30 DEM and slope, UTM 43N | `03_hydrogeology/06` |
| `model_grid/grid_1km_cells.parquet`, `grid_1km_arrays.npz`, `grid_meta.json` | 1 km grid: active cells, block, top, zone, bedrock | `04_model/03` |

All block tables share one layout: `Date, Year, Month, Day, 574_BANSUR … 587_UMREN`.

## Raw data

| Path | Contents |
|---|---|
| `GW/Shapefile/LGD_Blocks.geojson` | all-India block boundaries (298 MB; Alwar = `block_lgd` 574–587) |
| `GW/data/Rainfall_Rajasthan/*.pdf` | Rajasthan daily rainfall PDFs 2010–2025 |
| `GW/data/Rajasthan_gw_data/*.xlsx` | 13 district groundwater-level workbooks (Jaipur circle) |
| `GW/data/BDR/Alwar/*.pdf`, `Atalbdr/*.docx` (17), `nhpbdr 2023/*.docx` (42) | basic data reports of boreholes |
| `GW/data/CGRA_Reports/stateReport 2024-25.xlsx` | GEC 2024-25, sheet `GEC`, header in rows 7–9 |
| `GW/data/imd/netcdf/IMD_rain_0p25_YYYY.nc` | IMD rain 1901–2025 (variable `rain`, lat 6.5–38.5, lon 66.5–100) |
| `GW/data/imd_temp/{tmax,tmin}/YYYY.GRD` | IMD 1° temperature 1980–2024 (31 × 31 float32 per day; lat 7.5→37.5, lon 67.5→97.5; missing 99.9) |
| `GW/climate_forcing/Vimal_Mishra_CMIP6/Copy of India.tar.xz` | Mishra CMIP6 archive, 29 GiB; members `India/<model>/<scenario>/<PrecipData\|TMaxData\|TMinData>`; a second copy is in `MyDrive/Groundwater_Climate_Data/` |
| `GW/data/dem_copernicus/` | DEM tiles as downloaded |

## Stage outputs

| Path | Contents | Made by |
|---|---|---|
| `GW/data/Rainfall_Rajasthan/Matched_Block_Rainfall/`, `Rainfall_Audit_Minimum_Conflict_Rule/` | station rainfall, de-duplicated | `01_data/02` |
| `GW/data/Rajasthan_gw_data/Groundwater_Cleaning_According_to_User_Rules/` | cleaned seasonal levels (`WL_bgl`); wide table with `Hyd_Formation`, `RL (m)` | `01_data/03` |
| `GW/data/Rajasthan_gw_data/Well_Elevation_and_Head_Estimates/groundwater_measurements_with_estimated_head.csv` | DTW, coordinates, DEM elevation, head | `01_data/03` |
| `GW/data/gwl/diagnostics/Alwar_Source_Recovery/Step_2 … Step_18_*` | source recovery, 14-block domain (Step 14F), trends (Step 15), block summaries (Step 17) | `01_data/03`, `01_data/04` |
| `GW/climate_forcing/Mishra_Alwar_CORRECTED/` | raw corrected extraction (`cells/`, `blocks/`, `cells_clean/`), `extraction_log.csv`, `QC/` | `02_climate/03` |
| `GW/climate_forcing/Vimal_Mishra_CMIP6/SSP245_extracted/Alwar_grid_analysis/Area_weighted_spatial_selection/` | block–cell weights; `Alwar_block_grid_weights_CORRECTED.csv` | `02_climate/01`, `02_climate/03` |
| `GW/data/BDR/Alwar/…` | borehole database audits, lithology and hydrostratigraphy tables, sections | `03_hydrogeology/02`, `03` |
| `GW/MODFLOW_Alwar/…` | transient-model observation tables; geology map registers (`Step7ID4…`, `NATMO_…`, `G21F…`) | `04_model/02`, `03_hydrogeology/04`, `05` |
| `GW/model/alwar/runs/01_steady_plumbing_check/` | steady-state MODFLOW 6 files | `04_model/03` |
| `MyDrive/Alwar_BDR_Lithology_Inventory/`, `Groundwater_BDR_Analysis_Output/`, `Alwar_Verified_Data_Readiness_Audit/`, `Alwar_Groundwater_Calibration/` | outputs of the BDR PDF screening and first-pass model — these sit **outside** `gw_framework` | `03_hydrogeology/01`, `04_model/01` |

## Do not use for Alwar

- `GW/forcing_historical/`, `GW/climate_forcing/imd_hist_daily.nc`, `GW/inputs/*` (outside `inputs/alwar`), `GW/work/*`: demo runs for another area (21.75–22.75 N).
- `GW/data/nasa_power/22.125-27.875N_…`: stops at 27.875 N; not needed because PET uses Hargreaves.
- The first CMIP6 extraction folders listed in `DATA_LINEAGE_GAPS.md`.
