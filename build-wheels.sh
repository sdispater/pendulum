#!/bin/bash
PYTHON_VERSIONS="cp27-cp27m cp35-cp35m"

echo "Compile wheels"
for PYTHON in ${PYTHON_VERSIONS}; do
    /opt/python/${PYTHON}/bin/pip install -r /io/wheels-requirements.txt
    /opt/python/${PYTHON}/bin/pip wheel /io/ -w /io/wheelhouse/
done

echo "Bundle external shared libraries into the wheels"
for whl in /io/wheelhouse/*.whl; do
    auditwheel repair $whl -w /io/wheelhouse/
done

echo "Install packages and test"
for PYTHON in ${PYTHON_VERSIONS}; do
    /opt/python/${PYTHON}/bin/pip install pendulum --no-index -f /io/wheelhouse
    find ./io/tests | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
    /opt/python/${PYTHON}/bin/py.test /io/tests
    find ./io/tests | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
done
