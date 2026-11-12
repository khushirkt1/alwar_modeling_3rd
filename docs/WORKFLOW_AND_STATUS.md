# Workflow, results so far, and next steps

## Run order

Each notebook reads files written by earlier ones. A fresh start runs them in this order:

1. `01_data/01_data_inventory` (optional, read-only)
2. `01_data/02_station_rainfall_PDFs`
3. `01_data/03_groundwater_levels_cleaning_QC`
4. `01_data/04_study_domain_and_gw_trends`
5. `02_climate/01_cmip6_extraction_v1_SUPERSEDED` — only its section 3 (grid cells and block weights) is needed, to create `Alwar_block_grid_intersection_weights.csv`
6. `02_climate/03_climate_forcing_corrected`
7. `03_hydrogeology/06_gec_aquifer_zones_dem`
8. `04_model/03_grid_and_steady_state`

In parallel, for the aquifer structure: `03_hydrogeology/02` → `03` → `04` → `05`.
If the outputs already exist on Drive (they do for steps 1–7), start at the notebook you need.

## Results so far

**Groundwater levels and trends** (`01_data/04`)
- 473 of 502 wells lie inside the 14-block domain.
- 90 wells × 2 seasons = 180 series; 129 testable. 70 are significant under both Mann–Kendall and TFPW (FDR-corrected) and every one of them shows deepening (39 pre-monsoon, 31 post-monsoon).

**Climate** (`02_climate/03`; details in `CLIMATE_FORCING_methods.md`)
- IMD 1985–2014: 601 mm/yr, 87 % in Jun–Sep; Tmax 32.15 °C, Tmin 18.28 °C; Hargreaves PET ≈ 1,773 mm/yr.
- 13 GCMs × historical + 4 SSPs, cleaned and corrected with monthly QDM; 8 models have a realistic monsoon before QDM.

**GEC 2024-25** (`03_hydrogeology/06`)
- All 14 blocks over-exploited; stage of extraction 105–268 % (176 % overall); 87 % of extraction is irrigation.
- Rainfall-recharge factor 0.17–0.19 in alluvial blocks, 0.08–0.10 in the hard-rock blocks (Rajgarh, Reni, Thanagazi).
- GEC block areas differ from the GIS areas (ratio 0.75–1.66) → apply GEC as mm/yr rates.
- Specific yield implied by GEC deficit ÷ observed decline: about 0.015–0.09; starting value 0.04, range 0.01–0.12. Not usable for Umren, Thanagazi, Laxmangarh, Kishangarh Bas.

**Aquifer zones and grid** (`03_hydrogeology/06`, `04_model/03`)
- 474 wells: 282 alluvium, 104 alluvium over hard rock, 88 hard rock (Rajgarh 56 %, Thanagazi 76 % hard rock).
- DEM 182–775 m. Grid 133 × 111 cells of 1 km, 7,805 active; zones: alluvium 61 %, hard rock 27 %, alluvium over hard rock 13 %.

**Not verified yet**
- Layer thicknesses, K and Sy in the model are placeholders.
- No hydraulic parameter from the BDR PDFs is verified; only the CGWB transmissivity range 27–662 m²/d.
- `04_model/01` is a synthetic test, not an Alwar model.

## Next steps

1. **Run and review `04_model/03`** (grid map, convergence, heads against 2011–2014 observations).
2. **Layer geometry from boreholes:** use `Step6F_Borehole_Lithology_Elevation_Database.csv` and the hydrostratigraphic intervals (`03_hydrogeology/02`, `03`) to replace the placeholder thicknesses — depth to hard rock per borehole, interpolated within the alluvial zones.
3. **Pumping through time:** collect earlier GEC rounds (2004, 2009, 2011, 2013, 2017, 2020, 2022, 2023) and build `pumping_by_block.csv` in mm/yr.
4. **Recharge model:** daily soil-water balance per block and land-use class with IMD forcing and Hargreaves PET; check it against the GEC rainfall-recharge factors. Land use and soils still have to be chosen (for example ESA WorldCover and SoilGrids).
5. **Transient model:** seasonal stress periods (monsoon Jun–Oct, non-monsoon Nov–May), observation table from `04_model/02`, head-dependent boundaries from observed heads.
6. **Calibration with PEST++ IES** on heads, seasonal swing and the 70 robust Sen trends; hold out recent years.
7. **Scenarios:** climate on/off × pumping on/off for attribution; then 13 GCMs × SSPs × pumping pathways, reported for all 13 models and for the 8 good-monsoon models.
8. **Tidy Drive:** move the first-extraction climate folders into `_superseded_wrong_cells/`; move the four output folders outside `gw_framework` into it; delete one of the two 31 GB archive copies.
