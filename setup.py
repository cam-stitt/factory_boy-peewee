#!/usr/bin/env python

import sys

from setuptools import setup

if sys.version_info[0:2] < (2, 7):  # pragma: no cover
    test_loader = 'unittest2:TestLoader'
else:
    test_loader = 'unittest:TestLoader'

setup(
    name='factory_boy-peewee',
    version='0.0.3',
    description='peewee support for factory_boy',
    author='Cameron Stitt',
    author_email='cameron@cam.st',
    url='https://github.com/cam-stitt/factory_boy-peewee',
    packages=['factory_peewee'],
    install_requires=['factory_boy', 'peewee'],
    test_suite='tests',
    test_loader=test_loader,
)
