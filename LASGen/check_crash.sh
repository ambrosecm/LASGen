#!/bin/bash


crash_dir=""
program_file="$crash_dir/decompileActions"

# Final merged file path
output_file="$crash_dir/crashes_combined.bt"

# Clear existing content (if any)
> "$output_file"

# Iterate through all files in the crashes directory
for file in $crash_dir/output/default/crashes/*; do
    # Add separator mark (file name)
    echo -e "\n\n[ Backtrace for: $file ]" >> "$output_file"
    # Run gdb and append the results
    gdb --batch -ex "run" -ex "bt" --args $program_file "$file" >> "$output_file" 2>&1
done