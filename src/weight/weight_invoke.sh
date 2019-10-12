#!/bin/sh

DEBUG_LEVEL=0

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`

IN_FILE_PLAN=$CONFIG_PROFILE_DATA_LOC/weight-data/weight-data.csv
OUT_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/weight-reports/weight-reports-ticker-only.csv
OUT_FILE_2=$CONFIG_PROFILE_REPORTS_LOC/weight-reports/weight-reports-sort-units.csv
OUT_FILE_3=$CONFIG_PROFILE_REPORTS_LOC/weight-reports/weight-reports-sort-name.csv

# phase 2
# python -m pdb weight_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
python weight_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}
