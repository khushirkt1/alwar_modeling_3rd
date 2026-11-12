# Alwar climate forcing — methods and decisions (completed 2026-11-04)

Domain: 14 blocks of Alwar (LGD 574–587), area-weighted block-daily series.
Notebook: `notebooks/02_climate/03_climate_forcing_corrected.ipynb`.

## 1. Observed (IMD)
- Rain: IMD 0.25° gridded daily (Pai et al. 2014), 1951–2025, 25 cells.
- Tmax/Tmin: IMD 1° gridded daily, 1980–2024 (cells 27.5N/76.5E, 28.5N/76.5E, 27.5N/77.5E). Grid orientation verified (Alwar Jan 21.2 °C, May 40.5 °C).
- Weights: polygon–cell area intersection in UTM 43N; 100% block coverage.
- 1985–2014, 14-block mean: P 601 mm/yr (Jun–Sep 87%), Tmax 32.15 °C, Tmin 18.28 °C; block P 523 (Tijara) – 652 (Kathumar) mm.
- Files: `inputs/alwar/climate_obs/IMD_{rain,tmax,tmin,pet_hs}_AlwarBlocks.csv`

## 2. CMIP6 source
- Mishra et al. (2020, Sci. Data) bias-corrected (EQM) South Asia CMIP6, 0.25°, 13 GCMs: ACCESS-CM2, ACCESS-ESM1-5, BCC-CSM2-MR, CanESM5, EC-Earth3, EC-Earth3-Veg, INM-CM4-8, INM-CM5-0, MPI-ESM1-2-HR, MPI-ESM1-2-LR, MRI-ESM2-0, NorESM2-LM, NorESM2-MM; historical 1951–2014, SSP1-2.6/2-4.5/3-7.0/5-8.5 2015–2100.
- Extraction: 22 cells (76.125–77.125 E, 27.125–28.125 N) matched by lon/lat to the file header. The earlier extraction was offset by 3 columns (≈ 0.75° north) and is discarded.
- Cleaning: 625 source fill values (−273.15 °C = 0 K) interpolated in time (max gap 5 days); 10,000 cell-days with Tmax < Tmin swapped (artefact of univariate EQM, mostly CanESM5/INM, Nov–Jan); 29 Feb added for no-leap models (BCC-CSM2-MR, CanESM5, INM-CM4-8, INM-CM5-0, NorESM2-LM, NorESM2-MM) with T = mean of neighbours, P = 0. Tmax > 52 °C (392 block-days, late-century SSP3-7.0/5-8.5) kept and flagged.
- Files (dataset correction only): `inputs/alwar/climate_cmip6/`

## 3. Evaluation against IMD, 1985–2014 (dataset version)
- Tmax/Tmin bias within ±0.3 °C, PET within ±1.5 %, annual P within ±15 % (except NorESM2-MM +26 %).
- Seasonal timing of rain is NOT corrected by the dataset: Jun–Sep share 0.20 (ACCESS-ESM1-5), 0.34 (CanESM5), 0.49 (ACCESS-CM2), 0.59 (MRI-ESM2-0, NorESM2-LM) vs IMD 0.87. Temperature cycles are correctly timed (dates verified), so this is a model monsoon deficiency, not a date error.

## 4. Second-stage correction: monthly QDM (Cannon et al. 2015) — final forcing
- Per block, per calendar month; calibration IMD vs model historical 1985–2014; 30-year moving window per target decade.
- Rain: multiplicative QDM, wet threshold 0.1 mm, change ratio capped ×5 (1.1 % of values); then wet-day frequency adaptation: target frequency = IMD frequency × the model's relative change in frequency; smallest excess wet days set to 0, month-decade total preserved (largest change in totals 0.07 %).
- Temperature: QDM on Tmean (additive) and diurnal range (multiplicative); Tmax/Tmin rebuilt, so no inversions are possible. Temperature change preserved within 0.07 °C.
- After QDM, all models: P 590–614 mm/yr, Jun–Sep 0.87, cycle r = 1.0.
- QDM annual rain changes match "model monthly changes applied to IMD seasons" (e.g. EC-Earth3-Veg +35 % vs expected +38 %); raw annual changes were distorted by each model's own seasons.
- SSP2-4.5, 2071–2100 rain change (QDM): ACCESS-CM2 +58, ACCESS-ESM1-5 +153, BCC-CSM2-MR +20, CanESM5 +125, EC-Earth3 +30, EC-Earth3-Veg +35, INM-CM4-8 +45, INM-CM5-0 +72, MPI-ESM1-2-HR +81, MPI-ESM1-2-LR +17, MRI-ESM2-0 +2, NorESM2-LM +39, NorESM2-MM −2 %. Tmax change +0.9 to +3.4 °C.
- Files: `inputs/alwar/climate_cmip6_qdm/<scenario>/<model>_<scenario>_{PrecipData,TMaxData,TMinData,PET_HS}_AlwarBlocks.csv`; `model_subsets.csv`; backup of the QDM rain before the wet-day step in `_before_wetday_fix/`.

## 5. Ensemble decision
- Main results: all 13 QDM models. Robustness check: the 8 "good-monsoon" models (raw Jun–Sep share ≥ 0.75 and cycle r ≥ 0.86): BCC-CSM2-MR, EC-Earth3, EC-Earth3-Veg, INM-CM4-8, INM-CM5-0, MPI-ESM1-2-HR, MPI-ESM1-2-LR, NorESM2-MM.
- Report that the ACCESS-ESM1-5 and CanESM5 rain changes after QDM are large because their baseline monsoon is very weak.

## 6. PET
- Hargreaves–Samani (FAO-56 extraterrestrial radiation at the block centroid latitude) for both IMD and CMIP6, because the GCM files contain only P, Tmax and Tmin. IMD 1985–2014 PET ≈ 1,773 mm/yr.

## QC reports
`climate_forcing/Mishra_Alwar_CORRECTED/QC/01…12_*.csv`

## Relation to the first investigation
`02_climate/02_cmip6_temperature_QC_v1_SUPERSEDED.ipynb` examined Tmax < Tmin reversals and −273.15 °C sentinel values in the first extraction.
Both phenomena are real properties of the dataset and also appear in the correct cells, but the counts, dates and maps in that notebook refer to cells north of Alwar and should not be quoted.
