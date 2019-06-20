#!/bin/sh
tail -n +2 "project.py" > "project.tmp" && mv "project.tmp" "project.py"
echo 'from __init__ import init_db' > temp_file.py
cat project.py >> temp_file.py
mv temp_file.py project.py