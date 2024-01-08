#!/bin/bash

# Specify the directory to monitor
directory_to_monitor="captured/video"

# Extensions to check for
extensions=("mp4" "avi" "mkv" "mpeg4")

# Get the list of files with specified extensions
files=$(find "$directory_to_monitor" -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mkv" -o -iname "*.mpeg4" \))

# Iterate through the files
for file in $files; do
    echo "New file added: $file"
    
    # Trigger the Python script with the new file path as an argument
    # python3 /path/to/your/check_files.py "$file"
done
