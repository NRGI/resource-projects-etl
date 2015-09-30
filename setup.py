from setuptools import setup

setup(
    name='resource_projects_etl',
    version='0.0.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    package_dir = {'': 'modules'},
    py_modules=['taglifter', 'settings'],
    url='https://github.com/NRGI/resource-projects-etl',
    description='',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    ],
    install_requires=['cove', 'pandas', 'rdflib', 'countrycode'],
)
