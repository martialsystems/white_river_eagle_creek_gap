# Methodology: Eagle Creek plus Nora and Fall Creek versus Nora-plus-Fall-Creek at Centerton

Question: Does lagged Eagle Creek (Q) (plus Nora and Fall Creek) beat Nora-plus-Fall-Creek at Centerton on the same WY2019 to 2020 split?

Live science is `8e4fdca`. Yes on RMSE: 1,607 vs 1,734 vs 1,795 vs cited NWM 2,414. Nora-plus-Fall-Creek matches locked `962d503` on this matrix. MAE went the other way: 823 vs 791 vs 810. RMSE increment is Eagle Creek. Typical error did not improve. White Lick still sits on that stretch.

Features are lag-1 USGS daily mean 00060 at Nora (03351000), Fall Creek at Millersville (03352500), and EAGLE CREEK AT INDIANAPOLIS, IN (03353500). Label is WHITE RIVER NEAR CENTERTON, IN (03354000). Persistence is lag-1 00060 at Centerton. Nora-plus-Fall-Creek is the two-feature control. Indianapolis is not a feature.

03353451 EAGLE CREEK BELOW RESERVOIR AT INDIANAPOLIS, IN starts 2016-10-26. 03353200 Zionsville has three gaps. 03353600 is Little Eagle Creek. Empty or late 03353500 00060 stops. No alternate.

Cited Fall Creek Centerton Nora+FC 1,734 (`962d503`) and NWM Centerton 2,414 (`fa2e315`) are not recomputed. This repo does not download NWM.

OLS weight 3.27 is not a pour. MAE getting worse is not a closed reach.

## Layers

| Layer | Role | Source |
|-------|------|--------|
| Feature | lag-1 00060 | NWIS 03351000 Nora |
| Feature | lag-1 00060 | NWIS 03352500 FALL CREEK AT MILLERSVILLE, IN |
| Feature | lag-1 00060 | NWIS 03353500 EAGLE CREEK AT INDIANAPOLIS, IN |
| Label | 00060 | NWIS 03354000 Centerton |
| Split | same as Fall Creek / Anderson-Nora / NWM-error | Train through 2018-09-30, hold out 2018-10-01 to 2020-12-31 |

Lag locked at 1 calendar day. Train-only OLS. No 2026 overlay.

## Figures

1. Holdout hydrograph at Centerton: observed 00060, target lag 1 d, Nora+Fall Creek, Nora+Fall Creek+Eagle Creek. cfs.
2. Scatter of Nora+Fall Creek OLS contribution versus Eagle Creek OLS contribution.

## Claims

Allowed: lagged Eagle Creek 00060 plus Nora and Fall Creek versus Nora-plus-Fall-Creek at Centerton; 03353500 as the official Eagle Creek site with a clean daily record; citing Fall Creek and NWM RMSEs; RMSE yes with MAE worse.

Banned: P as a forecast; HAND as a FIRM; lag-scatter as inundation; inverting Q to feet; a third figure; restamping Fall Creek or NWM-error; calling 03353600 Eagle Creek; inventing a tributary when 00060 is empty or late; treating MAE-worse as a closed reach.
