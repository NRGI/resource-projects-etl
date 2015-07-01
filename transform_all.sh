#!/bin/bash
set -e
for f in process/*; do
    cd $f
    if [ -a transform.py ]; then
        python3 transform.py
    fi
    cd ../..
done
