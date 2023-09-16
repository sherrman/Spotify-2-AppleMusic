#!/usr/bin/env bash

for csv in *.csv; do
    if [[ $csv == *_itunes-version.csv ]]; then
        continue
    fi
    if [ -r "${spotify/.csv/_itunes-version.csv}" ]; then
        continue
    fi

    python3 ../getitunesid.py $csv
done
