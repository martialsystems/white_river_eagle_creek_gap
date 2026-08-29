# Operator checklist

1. Live RMSE is 1,607 vs 1,734 vs 1,795 vs cited NWM 2,414. MAE 823 vs 791. Do not re-fit.
2. Eagle Creek site is 03353500 EAGLE CREEK AT INDIANAPOLIS, IN. Below-reservoir 03353451 starts late. Little Eagle is a different creek.
3. Lag is 1 calendar day. Train-only OLS. Same holdout as Fall Creek / NWM-error / Anderson-Nora.
4. Control is Nora-plus-Fall-Creek (matches 962d503). Cite NWM 2,414. Do not download NWM.
5. Two figures: Centerton hydrograph; stem vs Eagle Creek contributions. Weight 3.27 is OLS, not a pour. cfs, not feet. No 2026.
6. Hydrology gist only, not gist 1.
7. Empty or late Eagle Creek 00060 stops. Do not invent a tributary.
8. MAE worse is not a closed reach. White Lick still open.
