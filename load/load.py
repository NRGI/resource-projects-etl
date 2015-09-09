"""
Currently requires the environment variable DBA_PASS for the password of the
dba user on the virtuoso server. e.g.
    DBA_PASS=dba python disambig.py
"""

import os
#import requests
#from requests.auth import HTTPDigestAuth
import subprocess
import urllib.parse


data_dir = '../data'

for f in os.listdir(data_dir):
    if f.endswith('.ttl'):
        slug = f[:-4]
        graphuri = 'http://staging.resourceprojects.org/' + slug

        # Call curl in a subprocess, as requests doesn't work with large files.
        subprocess.check_call([
            'curl',
            '-T',
            os.path.join(data_dir, f),
            'http://localhost:8890/sparql-graph-crud-auth?'+urllib.parse.urlencode({'graph' : graphuri}),
            '--user',
            'dba:{}'.format(os.environ['DBA_PASS'])
        ])

        #with open(os.path.join(data_dir, f), 'rb') as fp:
            #r = requests.put('http://localhost:8890/sparql-graph-crud-auth',
            ##'http://requestb.in/1mfng7t1',
            #    params = {'graph': graphuri},
            #    auth=HTTPDigestAuth('dba', os.environ['DBA_PASS']),
            #    data=fp
            #)
