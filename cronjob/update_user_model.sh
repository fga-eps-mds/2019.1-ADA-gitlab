#!/bin/sh
tail -n +3 "user.py" > "user.tmp" && mv "user.tmp" "user.py"
echo 'from __init__ import init_db\nfrom project import Project' > temp_file.py
cat user.py >> temp_file.py
mv temp_file.py user.py