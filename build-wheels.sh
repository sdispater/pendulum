#!/bin/bash
PYTHON_VERSIONS="cp27-cp27m cp34-cp34m cp35-cp35m cp36-cp36m cp37-cp37m"

POETRY_PYTHON="cp37-cp37m"
POETRY_VENV="/opt/python/poetry"
echo "Create Poetry's virtualenv"
/opt/python/${POETRY_PYTHON}/bin/pip install virtualenv
/opt/python/${POETRY_PYTHON}/bin/virtualenv --python /opt/python/${POETRY_PYTHON}/bin/python ${POETRY_VENV}
${POETRY_VENV}/bin/pip install poetry --pre

RELEASE=$(sed -n "s/__version__ = \"\(.*\)\"/\1/p" /io/pendulum/__version__.py)

echo "Compile wheels"
for PYTHON in ${PYTHON_VERSIONS}; do
    cd /io
    /opt/python/${POETRY_PYTHON}/bin/virtualenv --python /opt/python/${PYTHON}/bin/python /opt/python/venv-${PYTHON}
    . /opt/python/venv-${PYTHON}/bin/activate
    ${POETRY_VENV}/bin/poetry install -v
    ${POETRY_VENV}/bin/poetry build -v
    mv dist/*-${RELEASE}-*-linux_*.whl wheelhouse/
    deactivate
    cd -
done

echo "Bundle external shared libraries into the wheels"
for whl in /io/wheelhouse/pendulum-${RELEASE}-*-linux_*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

echo "Install packages and test"
for PYTHON in ${PYTHON_VERSIONS}; do
    . /opt/python/venv-${PYTHON}/bin/activate
    pip install pendulum==${RELEASE} --no-index --find-links /io/wheelhouse
    find ./io/tests | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
    pytest /io/tests -W ignore
    find ./io/tests | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
    deactivate
done
