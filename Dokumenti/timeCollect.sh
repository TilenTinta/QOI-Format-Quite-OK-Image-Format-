#!/bin/bash

# Create an array to hold the times
times=()

# Loop through the files from kodim01 to kodim24
for i in $(seq -w 1 24); do
  # Construct the filenames
  qoi_file="kodim${i}.qoi"
  png_file="kodim${i}.png"
  
  # Run the command and collect the time
  result=$( { time ./qoiconv "$qoi_file" "$png_file"; } 2>&1 )
  
  # Extract the real time from the result
  real_time=$(echo "$result" | grep real | awk '{print $2}')
  
  # Add the time to the array
  times+=("$real_time")
  
  # Print the time for this iteration
  echo "Time for $qoi_file: $real_time"
done

# Print all the collected times
echo "Collected times:"
for i in "${!times[@]}"; do
  echo "kodim$(printf "%02d" $((i + 1))).qoi: ${times[$i]}"
done
