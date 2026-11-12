"""Single place for the Google Drive paths used by the notebooks.

New code should import paths from here instead of typing them again::

    from alwar_gw import paths as P
    df = pd.read_csv(P.GEC_BLOCKS)

The notebooks split from the original working notebook still contain their own
hard-coded paths; they point to the same locations.
"""
from pathlib import Path

DRIVE = Path("/content/drive/MyDrive")
GW = DRIVE / "gw_framework"                      # project root on Drive

# ── raw data ────────────────────────────────────────────────────────────────
DATA = GW / "data"
BLOCKS_ALL_INDIA = GW / "Shapefile" / "LGD_Blocks.geojson"      # 298 MB
RAINFALL_PDFS = DATA / "Rainfall_Rajasthan"
GW_EXCEL = DATA / "Rajasthan_gw_data"
BDR = DATA / "BDR" / "Alwar"
GEC_WORKBOOK = DATA / "CGRA_Reports" / "stateReport 2024-25.xlsx"
IMD_RAIN_NC = DATA / "imd" / "netcdf"            # IMD_rain_0p25_YYYY.nc
IMD_TEMP_GRD = DATA / "imd_temp"                 # tmax/YYYY.GRD, tmin/YYYY.GRD
MISHRA = GW / "climate_forcing" / "Vimal_Mishra_CMIP6"
MISHRA_ARCHIVE = MISHRA / "Copy of India.tar.xz"
MISHRA_CORRECTED = GW / "climate_forcing" / "Mishra_Alwar_CORRECTED"

# ── groundwater levels and trends (outputs of notebooks 01_data/03 and 04) ──
HEADS_ALL = (GW_EXCEL / "Well_Elevation_and_Head_Estimates"
             / "groundwater_measurements_with_estimated_head.csv")
WELLS_WIDE = (GW_EXCEL / "Groundwater_Cleaning_According_to_User_Rules"
              / "groundwater_cleaned_wide_source_preserved.csv")
TRENDS = DATA / "gwl" / "diagnostics" / "Alwar_Source_Recovery"
DOMAIN_OBS = (TRENDS / "Step_15_Spatial_Trend_Restriction"
              / "02_spatially_restricted_groundwater_observations.csv")
BLOCK_TRENDS = (TRENDS / "Step_17_Block_Level_Trend_Assessment"
                / "03_step17_block_season_summary.csv")

# ── model-ready inputs (the hand-off folder) ────────────────────────────────
ALWAR = GW / "inputs" / "alwar"
BLOCKS = ALWAR / "blocks.geojson"                # 14 blocks, EPSG:4326
DOMAIN = ALWAR / "domain.geojson"
CLIMATE_OBS = ALWAR / "climate_obs"              # IMD_<var>_AlwarBlocks.csv
CLIMATE_CMIP6 = ALWAR / "climate_cmip6"          # dataset bias correction only
CLIMATE_CMIP6_QDM = ALWAR / "climate_cmip6_qdm"  # + monthly QDM  ← use this
GEC = ALWAR / "gec"
GEC_BLOCKS = GEC / "gec_2024_25_blocks.csv"
AQUIFER = ALWAR / "aquifer"
DEM = ALWAR / "dem_alwar_utm43n_30m.tif"
SLOPE = ALWAR / "slope_alwar_deg.tif"
GRID = ALWAR / "model_grid"

# ── models ──────────────────────────────────────────────────────────────────
MODEL_RUNS = GW / "model" / "alwar" / "runs"
MODFLOW_ALWAR = GW / "MODFLOW_Alwar"             # folder used by the transient-prep notebook

# ── constants ───────────────────────────────────────────────────────────────
UTM = "EPSG:32643"
LGD_CODES = list(range(574, 588))
MODELS = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "EC-Earth3",
          "EC-Earth3-Veg", "INM-CM4-8", "INM-CM5-0", "MPI-ESM1-2-HR",
          "MPI-ESM1-2-LR", "MRI-ESM2-0", "NorESM2-LM", "NorESM2-MM"]
GOOD_MONSOON_MODELS = ["BCC-CSM2-MR", "EC-Earth3", "EC-Earth3-Veg", "INM-CM4-8",
                       "INM-CM5-0", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "NorESM2-MM"]
SCENARIOS = ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]


def cmip6_file(model, scenario, variable, qdm=True):
    """Path of one block-daily CMIP6 file.

    variable: 'PrecipData', 'TMaxData', 'TMinData' or 'PET_HS'.
    """
    base = CLIMATE_CMIP6_QDM if qdm else CLIMATE_CMIP6
    return base / scenario / f"{model}_{scenario}_{variable}_AlwarBlocks.csv"


def check(verbose=True):
    """Report which key inputs exist on Drive. Returns {name: bool}."""
    items = {
        "project root": GW, "blocks.geojson": BLOCKS, "IMD block climate": CLIMATE_OBS,
        "CMIP6 QDM forcing": CLIMATE_CMIP6_QDM, "GEC blocks": GEC_BLOCKS,
        "DEM": DEM, "model grid": GRID, "domain observations": DOMAIN_OBS,
    }
    out = {k: p.exists() for k, p in items.items()}
    if verbose:
        for k, ok in out.items():
            print(f"  {'OK     ' if ok else 'MISSING'} {k:22s} {items[k]}")
    return out
