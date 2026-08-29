# Copyright (c) 2026 Martial Systems LLC
"""Eagle Creek vs the Indianapolis to Centerton gap. Does not read p_sfha. Does not download NWM."""

from __future__ import annotations

from datetime import date

QUESTION = (
    "Does lagged Eagle Creek (Q) (plus Nora and Fall Creek) beat Nora-plus-Fall-Creek "
    "at Centerton on the same WY2019 to 2020 split?"
)

NORA_ID = "03351000"
NORA_NAME = "WHITE RIVER NEAR NORA, IN"
FALL_CREEK_ID = "03352500"
FALL_CREEK_NAME = "FALL CREEK AT MILLERSVILLE, IN"
EAGLE_CREEK_ID = "03353500"
EAGLE_CREEK_NAME = "EAGLE CREEK AT INDIANAPOLIS, IN"
CENTERTON_ID = "03354000"
CENTERTON_NAME = "WHITE RIVER NEAR CENTERTON, IN"
# Not features. Indianapolis would be more White River. Little Eagle is a different creek.
INDY_ID = "03353000"
LITTLE_EAGLE_ID = "03353600"
ZIONSVILLE_ID = "03353200"
BELOW_RESERVOIR_ID = "03353451"

LAG_DAYS = 1
MAX_FIGURES = 2
LIVE_START = date(2016, 10, 1)
LIVE_END = date(2020, 12, 31)
TRAIN_END = date(2018, 9, 30)
HOLDOUT_START = date(2018, 10, 1)

# Cited, not recomputed.
ANDERSON_NORA_CITATION = "58859be"
ANDERSON_NORA_RMSE_CFS = 970.78
FALL_CREEK_CITATION = "962d503"
FALL_CREEK_INDY_RMSE_CFS = 1264.63
FALL_CREEK_CENTERTON_NORA_FC_RMSE_CFS = 1734.27
NWM_CITATION = "fa2e315"
NWM_CENTERTON_RMSE_CFS = 2414.32
NWM_CENTERTON_PERS_RMSE_CFS = 1794.57

LOCKED_LIVE_COMMIT = ""
USER_AGENT = "MartialSystemsResearch/white_river_eagle_creek_gap"
NWIS_DV_URL = (
    "https://waterservices.usgs.gov/nwis/dv/?format=json&sites={site}"
    "&startDT={start}&endDT={end}&parameterCd=00060&siteStatus=all"
)
