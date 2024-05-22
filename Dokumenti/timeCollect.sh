#!/bin/bash

times=()

# Loop through the files from kodim01 to kodim24
for i in $(seq -w 1 24); do
  qoi_file="kodim${i}.qoi"
  png_file="kodim${i}.png"
  
  # command
  result=$( { time ./qoiconv "$qoi_file" "$png_file"; } 2>&1 )
  real_time=$(echo "$result" | grep real | awk '{print $2}')
  times+=("$real_time")
  echo "Time for $qoi_file: $real_time"
done

# Print
echo "Collected times:"
for i in "${!times[@]}"; do
  echo "kodim$(printf "%02d" $((i + 1))).qoi: ${times[$i]}"
done
