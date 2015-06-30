Docker container definition for loading data into virtuoso.

You will need a [virtuoso container running](https://github.com/NRGI/resourceprojects.org-frontend/#pre-requisites).

Then from this directory:

```
docker build -t rp-load .
cd ..
docker run --name rp-load --link virtuoso:virtuoso --volumes-from virtuoso -v `pwd`/data:/data --rm rp-load
```
