import subprocess

from pathlib import Path


def meson(*args):
    subprocess.call(["meson"] + list(args))


def _build():
    build_dir = Path(__file__).parent.joinpath("build")
    build_dir.mkdir(parents=True, exist_ok=True)

    meson("setup", build_dir.as_posix())
    meson("compile", "-C", build_dir.as_posix())
    meson("install", "-C", build_dir.as_posix())


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    try:
        _build()
    except Exception:
        print(
            "  Unable to build C extensions, "
            "Pendulum will use the pure python version of the extensions."
        )


if __name__ == "__main__":
    build({})
