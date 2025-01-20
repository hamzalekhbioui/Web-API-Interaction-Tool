#!/bin/bash

if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in the current directory."
    exit 1
fi

echo "Welcome to Article Metadata Formatter"
echo "--------------------------------------"
echo "Choose your search type:"
echo "1. DOI"
echo "2. Title"
echo "3. Author"
echo "--------------------------------------"

read -p "Enter your choice (1/2/3): " choice
case $choice in
    1)
        query_type="doi"
        ;;
    2)
        query_type="title"
        ;;
    3)
        query_type="author"
        ;;
    *)
        echo "Invalid choice. Please select 1, 2, or 3."
        exit 1
        ;;
esac

read -p "Enter the search value: " query_value

python3 main.py "$query_type" "$query_value"
