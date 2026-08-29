# Agent notes: white_river_eagle_creek_gap

Public GitHub. MIT. Question: Does lagged Eagle Creek (Q) (plus Nora and Fall Creek) beat Nora-plus-Fall-Creek at Centerton on the same WY2019 to 2020 split?

Yes on RMSE: 1,607 vs 1,734 vs 1,795 vs cited NWM 2,414. MAE 823 vs 791 vs 810. Nora-plus-Fall-Creek is the control and matches `962d503`. Not a closed reach.

Site: 03353500 EAGLE CREEK AT INDIANAPOLIS, IN. 03353451 starts late. Little Eagle Creek is a different creek. Empty or late 00060 stops. No alternate.

Do not restamp Fall Creek (`962d503` / `ccdf4ac`), NWM-error (`fa2e315` / `fbbe1fd`), or Anderson-Nora (`58859be`). Cite their RMSEs. Do not download NWM. Do not edit rain-stage, Nora HAND, FIM, HWM, or map-completion. Do not invert Q to feet. Do not open a sixth raster tree. Do not invent a tributary. Indianapolis is not in X. Hydrology gist only.

`ecgapforge/` GraphForge pin: no `p_sfha`, lag-1 locked, Eagle Creek 00060 fetch-or-stop (empty or late), no invented tributary, no NWM download.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
