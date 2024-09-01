#!/bin/bash

# Hardcoded directory path
dir="./posts/universalprior"

# Check if the directory exists
if [ ! -d "$dir" ]; then
    echo "Error: Directory $dir does not exist"
    exit 1
fi

# Loop through all .md files in the specified directory
for file in "$dir"/*.md; do
    if [ -f "$file" ]; then
        # Extract the date from the 5th line of the file
        date_line=$(sed -n '5p' "$file")
        # Remove the asterisks and convert the date format
        date=$(echo "$date_line" | sed 's/\*\*//g' | date -f - "+%Y-%m-%d" 2>/dev/null)
        
        # If date conversion fails, use a placeholder
        if [ $? -ne 0 ]; then
            date="2024-08-31"
            echo "Warning: Couldn't parse date in $file. Using placeholder."
        fi

        # Create the header with the extracted date
        header="---
title: minimalprior
subtitle: a spinoff
author: Jan Kirchner
author-url: \"https://universalprior.substack.com/\"
date: $date
---"

        # Create a temporary file
        temp_file=$(mktemp)
        
        # Write the header to the temporary file
        echo "$header" > "$temp_file"
        
        # Append the original file content to the temporary file, skipping the first 5 lines
        tail -n +6 "$file" >> "$temp_file"
        
        # Replace the original file with the temporary file
        mv "$temp_file" "$file"
        
        echo "Header added to $file with date: $date"
    fi
done

echo "Process completed"