#!/bin/bash

directory="../data/GRID"

find "$directory" -type f -name "*.mpg" > GRID_files.txt

echo "List of .mpg files saved to GRID_files.txt"
