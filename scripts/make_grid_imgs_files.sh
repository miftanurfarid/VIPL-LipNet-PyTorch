#!/usr/bin/env sh

directory="../data/GRID_imgs"

find "$directory" -type f -name "*.jpg" > imgs.txt

echo "List of .jpg files saved to imgs.txt"
