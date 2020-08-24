#!/bin/bash

cd /app/backend
source venv/bin/activate

if [ ! -e ./data/vid.db ]; then
    python3.8 initdb.py    
fi

python3.8 videocollector.py

