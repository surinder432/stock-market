#!/bin/sh

DEBUG_LEVEL=0

# IN_FILE_BSE=$PROJ_DATA_LOC/isin-data/isin-bse-500.csv
# IN_FILE_NSE=$PROJ_DATA_LOC/isin-data/isin-nse-500.csv

IN_FILE=$PROJ_DATA_LOC/screener-data/screener-data.csv
OUT_FILE_1=$PROJ_REPORTS_LOC/screener-reports/screener-reports-phase-1.csv

screener_invoke.py ${DEBUG_LEVEL} ${IN_FILE} ${OUT_FILE_1}
