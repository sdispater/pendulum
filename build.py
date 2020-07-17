import os
import shutil
import sys

from distutils.command.build_ext import build_ext
from distutils.core import Distribution
from distutils.core import Extension
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError


# C Extensions
with_extensions = os.getenv("PENDULUM_EXTENSIONS", None)

if with_extensions == "1" or with_extensions is None:
    with_extensions = True

if with_extensions == "0" or hasattr(sys, "pypy_version_info"):
    with_extensions = False

extensions = []
if with_extensions:
    extensions = [
        Extension("pendulum._extensions._helpers", ["pendulum/_extensions/_helpers.c"]),
        Extension("pendulum.parsing._iso8601", ["pendulum/parsing/_iso8601.c"]),
    ]


class BuildFailed(Exception):

    pass


class ExtBuilder(build_ext):
    # This class allows C extension building to fail.

    built_extensions = []

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            print(
                "  Unable to build the C extensions, "
                "Pendulum will use the pure python code instead."
            )

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            print(
                '  Unable to build the "{}" C extension, '
                "Pendulum will use the pure python version of the extension.".format(
                    ext.name
                )
            )


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    distribution = Distribution({"name": "pendulum", "ext_modules": extensions})
    distribution.package_dir = "pendulum"

    cmd = ExtBuilder(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        if not os.path.exists(output):
            continue

        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

    return setup_kwargs


if __name__ == "__main__":
    build({})
