import json
import os
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


#
# REQUIREMENTS
#
def parse_requirements(requirements):

    return [
        r.strip()
        for r in requirements
        if (
            not r.strip().startswith('#') and
            not r.strip().startswith('-e') and
            r.strip())
    ]


with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
    requirements = parse_requirements(f.readlines())


#
# CONFIG
#
with open(os.path.join(BASE_DIR, '.lily', 'config.json')) as f:
    config = json.loads(f.read())


# -- SETUP
setup(
    name=config['name'],
    description='Scaper and graph creator for Wiedza i Zycie articles content',
    url=config['repository'],
    version=config['version'],
    author='CoSphere Team',
    packages=find_packages(),
    install_requires=requirements,
    package_data={'': ['requirements.txt']},
    entry_points='''
        [console_scripts]
        scraper=wiedza_i_zycie.cli:cli
    ''',
    include_package_data=True)
