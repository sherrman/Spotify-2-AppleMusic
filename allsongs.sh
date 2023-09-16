#!/usr/bin/env bash

mkdir -p done
for itunes in *_itunes-version.csv; do
    spotify=${itunes/_itunes-version.csv/.csv}
    playlist=${itunes/-version.csv/-id.txt}
    echo "adding from $itunes ($playlist)"
    python3 ../addsongs.py $itunes
    if [ $? == 0 ]; then
        mv "$itunes" "$playlist" "$spotify" done/
    else
        echo "IMPORT ERROR $itunes"
    fi
done
