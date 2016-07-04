# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'pendulum/version.py')) as f:
        variables = {}
        exec(f.read(), variables)

        version = variables.get('VERSION')
        if version:
            return version

    raise RuntimeError('No version info found.')


__version__ = get_version()

setup(
    name='pendulum',
    license='MIT',
    version=__version__,
    description='Python datetimes made easy.',
    long_description=open('README.rst').read(),
    author='Sébastien Eustace',
    author_email='sebastien@eustace.io',
    url='https://github.com/sdispater/pendulum',
    download_url='https://github.com/sdispater/pendulum/archive/%s.tar.gz' % __version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'tzlocal',
        'pytz',
        'python-dateutil',
        'python-translate'
    ],
    tests_require=['pytest'],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
