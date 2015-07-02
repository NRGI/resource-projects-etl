#!/bin/bash
for f in process/*; do
    cd $f
    python3 transform.py
    cd ../..
done
