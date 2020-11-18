#!/bin/bash
set -e -x

cd $(dirname $0)

curl -fsS -o install-poetry.py https://raw.githubusercontent.com/sdispater/poetry/master/install-poetry.py
if [ $(uname -m) == 'i686' ]; then
    yum update
    curl -fsS -o rust-1.59.0-i686-unknown-linux-gnu.tar.gz https://static.rust-lang.org/dist/rust-1.59.0-i686-unknown-linux-gnu.tar.gz
    tar -xf rust-1.59.0-i686-unknown-linux-gnu.tar.gz && cd rust-1.59.0-i686-unknown-linux-gnu
    ./install.sh && cd ../
    curl -fsS -o openssl-1.1.1k.tar.gz https://ftp.openssl.org/source/openssl-1.1.1k.tar.gz
    tar -xzf openssl-1.1.1k.tar.gz && cd openssl-1.1.1k
    ./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib no-shared zlib-dynamic
    make && make install && cd ../
fi
export OLD_PATH=$PATH

for PYBIN in /opt/python/cp3*/bin; do
  if [ "$PYBIN" == "/opt/python/cp34-cp34m/bin" ]; then
    continue
  fi
  if [ "$PYBIN" == "/opt/python/cp35-cp35m/bin" ]; then
    continue
  fi
  if [ "$PYBIN" == "/opt/python/cp36-cp36m/bin" ]; then
    continue
  fi
  rm -rf build
  export PATH=${PYBIN}:$OLD_PATH
  POETRY_HOME=${PYBIN} ${PYBIN}/python install-poetry.py --preview -y
  export PATH=${PYBIN}/bin:$PATH
  poetry build -vvv
done

cd dist
for whl in *.whl; do
    auditwheel repair "$whl"
    rm "$whl"
done
