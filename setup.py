from setuptools import setup
import sys

with open('./requirements.txt') as requirements:
    install_requires = requirements.read().strip().splitlines()

setup(
    name='resource_projects_etl',
    version='0.0.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    package_dir = {'': 'modules'},
    py_modules=['taglifter'],
    url='https://github.com/NRGI/resource-projects-etl',
    description='',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    ],
    install_requires=install_requires
)
