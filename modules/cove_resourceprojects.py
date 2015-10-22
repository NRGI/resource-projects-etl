from taglifter import TagLifter
from collections import OrderedDict
from functools import partial
##requests doesn't work with large files, see below
#import requests
#from requests.auth import HTTPDigestAuth
import subprocess
import os
import json
import urllib.parse


def fetch(dataset):
    dataset.supplied_data.download()


def convert(dataset):
    if dataset.supplied_data.is_google_doc():
        main_source = None
    else:
        main_source = dataset.supplied_data.original_file.file.name

    tl = TagLifter(
        ontology="ontology/resource-projects-ontology.rdf",
        source=main_source,
        base="http://resourceprojects.org/",
        source_meta={}
    )

    if dataset.supplied_data.is_google_doc():
        with open(dataset.supplied_data.original_file.file.name) as fp:
            for entry in json.load(fp)['feed']['entry']:
                tl.source_meta = {"sheet": entry['title']['$t']}
                tl.load_data(os.path.join(dataset.supplied_data.upload_dir(), 'googledoc', entry['title']['$t']))
                tl.build_graph()
    else:
        tl.build_graph()

    tl.graph.serialize(
        format='turtle',
        destination=os.path.join(dataset.supplied_data.upload_dir(), 'output.ttl')
    )


def put_to_virtuoso(dataset, staging):
    ttl_filename = os.path.join(dataset.supplied_data.upload_dir(), 'output.ttl')
    prefix = 'staging.' if staging else ''
    graphuri = 'http://{}resourceprojects.org/{}'.format(prefix, dataset.name)

    # Call curl in a subprocess, as requests doesn't work with large files.
    #
    # Security considerations:
    # Beware adding user input to this call. check_call has shell=False by
    # default, which means it's not possible to eascape the shell. However,
    # user input could pass extra arguments / sensitive files to curl, so we
    # should be careful:
    # * ttl_filename is not from user input, so should be safe
    # * graphuri is urlencoded, so should be safe
    subprocess.check_call([
        'curl',
        '-T',
        ttl_filename,
        'http://virtuoso:8890/sparql-graph-crud-auth?' + urllib.parse.urlencode({'graph': graphuri}),
        '--digest',
        '--user',
        'dba:{}'.format(os.environ['DBA_PASS'])
    ])

    # This requests code doesn't work for files larger than about 1MB
    #with open(os.path.join(data_dir, f), 'rb') as fp:
    #    r = requests.put('http://localhost:8890/sparql-graph-crud-auth',
    #    #'http://requestb.in/1mfng7t1',
    #        params = {'graph': graphuri},
    #        auth=HTTPDigestAuth('dba', os.environ['DBA_PASS']),
    #        data=fp
    #    )

    # We're using shell=True here (and running virutoso SQL directly!), so must
    # trust prefix, graphuri and DBA_PASS. The only outside input to this are
    # DBA_PASS the pk used to construct graphuri, which are not user editable.
    # We must ensure this continues to be the case.
    subprocess.check_call('''
        echo "DB.DBA.RDF_GRAPH_GROUP_INS('http://{}resourceprojects.org/data/', '{}');" | isql virtuoso dba {} \
        '''.format(prefix, graphuri, os.environ['DBA_PASS']), shell=True)


def delete_from_virtuoso(dataset, staging):
    prefix = 'staging.' if staging else ''
    graphuri = 'http://{}resourceprojects.org/{}'.format(prefix, dataset.name)

    # Using curl here because we're already using it for putting.
    # If we want to switch to e.g. requests this part should work fine.
    subprocess.check_call([
        'curl',
        '-X',
        'DELETE',
        'http://virtuoso:8890/sparql-graph-crud-auth?' + urllib.parse.urlencode({'graph': graphuri}),
        '--digest',
        '--user',
        'dba:{}'.format(os.environ['DBA_PASS'])
    ])


def outputted_ttl(dataset):
     return dataset.supplied_data.upload_url() + 'output.ttl'
   


PROCESSES = OrderedDict([
    ('fetch', {
        'name': 'Fetched',
        'action_name': 'Fetch',
        'depends': None,
        'function': fetch,
        'main': True,
    }),
    ('convert', {
        'name': 'Converted',
        'action_name': 'Convert',
        'more_info_name': 'Outputted TTL',
        'more_info_link': outputted_ttl,
        'depends': 'fetch',
        'function': convert,
        'main': True
    }),
    ('staging', {
        'name': 'Pushed to staging',
        'action_name': 'Push to staging',
        'more_info_name': 'View on staging',
        'more_info_link': lambda x: os.environ.get('FRONTEND_STAGING_URL', ''),
        'depends': 'convert',
        'function': partial(put_to_virtuoso, staging=True),
        'reverse_id': 'rm_staging',
        'main': True
    }),
    ('live', {
        'name': 'Pushed to live',
        'action_name': 'Push to live',
        'depends': 'fetch',
        'more_info_name': 'View on live',
        'more_info_link': lambda x: os.environ.get('FRONTEND_LIVE_URL', ''),
        'function': partial(put_to_virtuoso, staging=False),
        'reverse_id': 'rm_live',
        'main': True
    }),
    ('rm_staging', {
        'name': 'Removed from staging',
        'action_name': 'Remove from staging',
        'depends': 'staging',
        'function': partial(delete_from_virtuoso, staging=True),
        'main': False
    }),
    ('rm_live', {
        'name': 'Removed from live',
        'action_name': 'Remove from live',
        'depends': 'live',
        'function': partial(delete_from_virtuoso, staging=False),
        'main': False
    }),
])
