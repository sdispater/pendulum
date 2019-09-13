#!/bin/bash
set -e -x

cd $(dirname $0)

curl -fsS -o get-poetry.py https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py
/opt/python/cp38-cp38/bin/python get-poetry.py --preview -y
rm get-poetry.py

for PYBIN in /opt/python/*/bin; do
  if [ "$PYBIN" == "/opt/python/cp34-cp34m/bin" ]; then
    continue
  fi
  rm -rf build
  "${PYBIN}/python" $HOME/.poetry/bin/poetry build -vvv
done

cd dist
for whl in *.whl; do
    auditwheel repair "$whl"
    rm "$whl"
done
