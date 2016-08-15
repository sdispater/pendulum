# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages, Extension
from distutils.errors import (CCompilerError, DistutilsExecError,
                              DistutilsPlatformError)
from distutils.command.build_ext import build_ext


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

# C Extensions
with_extensions = os.environ.get('PENDULUM_EXTENSIONS', '')

if with_extensions.lower() == 'false':
    with_extensions = False
else:
    with_extensions = True

if hasattr(sys, 'pypy_version_info'):
    with_extensions = False


extensions = []
if with_extensions:
    try:
        from Cython.Build import cythonize
        USE_CYTHON = True
    except ImportError:
        USE_CYTHON = False

    ext = '.pyx' if USE_CYTHON else '.c'

    extensions = [
        Extension('pendulum._extensions.tz.cbreakdown',
                  ['pendulum/_extensions/tz/cbreakdown' + ext],
                  extra_compile_args=['-Wno-unused-function']),
    ]

    if USE_CYTHON:
        extensions = cythonize(extensions)


class BuildFailed(Exception):

    pass


class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError,
                DistutilsPlatformError, ValueError):
            raise BuildFailed()


kwargs = dict(
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
    ],
    include_package_data=True,
    tests_require=['pytest'],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

if extensions:
    kwargs['ext_modules'] = extensions
    kwargs['cmdclass'] = dict(build_ext=ve_build_ext)


try:
    setup(**kwargs)
except BuildFailed:
    print("************************************************************")
    print("Cannot compile C accelerator module, use pure python version")
    print("************************************************************")
    del kwargs['ext_modules']
    del kwargs['cmdclass']
    setup(**kwargs)
