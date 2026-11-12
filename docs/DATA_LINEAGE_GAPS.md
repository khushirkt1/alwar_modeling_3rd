# Files the notebooks read but no notebook creates

Found by scanning the code of all 367 original cells (an automatic scan, checked by hand; treat it as a guide).
For a reproducible thesis, each derived file below needs either the code that made it added to a notebook, or a
short note saying how it was produced.

## Derived files with no producing cell

| File | Read in | Probably produced by |
|---|---|---|
| `Alwar_BDR_Extracted_Database.xlsx` | `03_hydrogeology/02` | extraction of the Atal and NHP Word files (Steps 1–3) |
| `Borehole_Master_Combined.csv` | `03_hydrogeology/02` | same extraction |
| `Lithology_Intervals_Combined.csv`, `Lithology_Interval_QC.csv` | `03_hydrogeology/02` | same extraction |
| `NHP_Docx_vs_Excel_Coordinate_QC.csv`, `Water_Bearing_Zones_NHP.csv` | `03_hydrogeology/02` | same extraction |
| `11_Parsed_Original_Lithology_Intervals.csv` | `03_hydrogeology/02` (Step 4H) | parsing step between Step 4D and Step 4H |
| `Alwar_Accepted_Lithology_Intervals.csv` | `03_hydrogeology/02`, `03` | acceptance step after the lithology review (Step 5) |
| `Alwar_Lithology_Classified_Intervals_Final.csv` | `03_hydrogeology/02`, `03` | lithology classification (Step 6A) |
| `Step6B_Borehole_Coordinates_For_DEM.csv` | `03_hydrogeology/02`, `03` | coordinate table for DEM sampling (Step 6B) |
| `Step6C_SRTM30m_Borehole_Elevations.csv` | `03_hydrogeology/02` | SRTM 30 m sampling (Step 6C) |
| `Step7ID_Interval_Conceptual_Interpretation.csv` and the other `Step7ID_*` registers | `03_hydrogeology/05` | conceptual interpretation step (Step 7I-D) |
| `Step7ID4F2_Feature_Control_Point_Register.xlsx`, `Step7ID4F3_OSM_Reference_Coordinates_Candidates.*` | `03_hydrogeology/04` | earlier control-point steps (7I-D4 F2/F3) |

## External source files (download or copy by hand)

| File | What it is |
|---|---|
| `Alwar_Hydrogeological_Atlas_2013.pdf` | district hydrogeological atlas (Plate IV = geological map) |
| `Alwar_Plate_IV_Geological_Map_HighRes.png` | Plate IV exported from the atlas |
| `NATMO_Alwar_District_Planning_Map.jpg` | NATMO district planning map |
| `600_DRM_data_gov_in_11072022_SUBMITTED.csv` | GSI catalogue from data.gov.in |
| `Rajasthan_Aquifer_Mapping_Final_Report.pdf` | aquifer mapping report (the download cell timed out in the source notebook) |
| `stateReport 2024-25.xlsx` | GEC 2024-25 block report (IN-GRES) |
| `Copy of India.tar.xz` | Mishra et al. CMIP6 archive (Zenodo) |
| `LGD_Blocks.geojson` | all-India block boundaries |

## Climate outputs that must not be used

Folders on Drive written by the first extraction (wrong grid cells): `Alwar_daily_extracted/`, `Alwar_daily_leapday_corrected/`,
`Alwar_daily_extracted_REBUILT/`, `Alwar_block_daily_forcing/`, `Alwar_block_daily_forcing_REBUILT/`,
`Alwar_block_daily_weighted_REBUILT/`, and the `Climate_Indicators/` results derived from them.
Consider moving them into one folder named `_superseded_wrong_cells/`.
