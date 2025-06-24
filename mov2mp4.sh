#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input.mov speed_factor"
    exit 1
fi

input_file=$1
speed_factor=$2

# Extract the base name of the input file (without extension)
base_name=$(basename "$input_file" .mov)

# Construct the output file name
output_file="${base_name}.mp4"

# Run ffmpeg with the provided speed factor
ffmpeg -i "$input_file" -filter:v "setpts=PTS/$speed_factor" "$output_file"

echo "Output saved to $output_file"
