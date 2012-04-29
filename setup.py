# -*- coding: utf-8 -*-
"""
Setuptools script for pp-gdata-helper (pp.gdata.helper)

"""
from setuptools import setup, find_packages

Name = 'pp-gdata-helper'
ProjectUrl = ""
Version = "1.0.1dev"
Author = ''
AuthorEmail = 'everyone at pythonpro dot co dot uk'
Maintainer = ''
Summary = ' pp-gdata-helper '
License = ''
Description = Summary
ShortDescription = Summary

needed = [
    'sphinx',  # for docs generation.
    'evasion-common',
    "cmdln",
    "gdata",

    # This provides vcard and icalendar read/write abilities.
    'vobject',
]

test_needed = [
]

test_suite = 'pp.gdata.helper.tests'

EagerResources = [
    'pp',
]

# Example including shell script out of scripts dir
ProjectScripts = [
#    'pp.gdata.helper/scripts/somescript',
]

PackageData = {
    '': ['*.*'],
}

# Example console script and paster template integration:
EntryPoints = {
    'console_scripts': [
        'oauth-admin = pp.gdata.helper.scripts.main:main',
    ],
}


setup(
    url=ProjectUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    classifiers=[
      "Programming Language :: Python",
    ],
    license=License,
    scripts=ProjectScripts,
    install_requires=needed,
    tests_require=test_needed,
    test_suite=test_suite,
    include_package_data=True,
    packages=find_packages(),
    package_data=PackageData,
    eager_resources=EagerResources,
    entry_points=EntryPoints,
    namespace_packages=['pp', 'pp.gdata'],
)
