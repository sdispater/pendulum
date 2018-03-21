import os
import sys


from distutils.core import Extension

from distutils.errors import (CCompilerError, DistutilsExecError,
                              DistutilsPlatformError)
from distutils.command.build_ext import build_ext


# C Extensions
with_extensions = os.getenv('PENDULUM_EXTENSIONS', None)

if with_extensions == '1' or with_extensions is None:
    with_extensions = True

if with_extensions == '0' or hasattr(sys, 'pypy_version_info'):
    with_extensions = False

extensions = []
if with_extensions:
    extensions = [
        Extension('pendulum._extensions._helpers',
                  ['pendulum/_extensions/_helpers.c']),
    ]


class BuildFailed(Exception):

    pass


class ExtBuilder(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
           pass

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError,
                DistutilsPlatformError, ValueError):
            pass


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update({
        'ext_modules': extensions,
        'cmdclass': {
            'build_ext': ExtBuilder
        }
    })
