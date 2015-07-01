set -e
for f in process/*; do
    cd $f
    if [ -a transform.py ]; then
        python transform.py
    fi
    cd ../..
done
