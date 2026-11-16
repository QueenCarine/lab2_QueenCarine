#!/bin/bash

mkdir -p archive


if [ ! -f grades.csv ]; then
    echo "Error: grades.csv is not found in $(pwd)" >&2
    exit 1
fi

timestamp=$(date +"%Y%m%d-%H%M%S")
archived="grades_${timestamp}.csv"


mv grades.csv "archive/${archived}"
touch grades.csv

echo "[$timestamp] Original: grades.csv | Archived: archive/${archived}" >> organizer.log

echo "Archived grades.csv as archive/${archived}"