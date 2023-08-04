# This file is part of orator
# https://github.com/sdispater/orator

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015 Sébastien Eustace

PENDULUM_RELEASE := $$(sed -n -E "s/VERSION = \"(.+)\"/\1/p" pendulum/version.py)

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies
setup: setup-python

# test your application (tests in the tests/ directory)
test:
	@py.test --cov=pendulum --cov-config .coveragerc tests/ -sq

linux_release: wheels_x64 wheels_i686

release: wheels_x64 wheels_i686 wheel

publish:
	@poetry publish --no-build

tar:
	python setup.py sdist --formats=gztar

wheel:
	@poetry build -v

wheels_x64: build_wheels_x64

wheels_i686: build_wheels_i686

build_wheels_x64:
	docker pull quay.io/pypa/manylinux1_x86_64
	docker run --rm -v `pwd`:/io quay.io/pypa/manylinux1_x86_64 /io/build-wheels.sh

build_wheels_i686:
	docker pull quay.io/pypa/manylinux1_i686
	docker run --rm -v `pwd`:/io quay.io/pypa/manylinux1_i686 /io/build-wheels.sh

# run tests against all supported python versions
tox:
	@tox


lint-rust:
	cargo fmt --version
	cargo fmt --all -- --check
	cargo clippy --version
	cargo clippy --tests -- \
		-D warnings \
		-W clippy::pedantic \
		-W clippy::dbg_macro \
		-W clippy::print_stdout \
		-A clippy::cast-possible-truncation \
		-A clippy::cast-possible-wrap \
		-A clippy::cast-precision-loss \
		-A clippy::cast-sign-loss \
		-A clippy::doc-markdown \
		-A clippy::float-cmp \
		-A clippy::fn-params-excessive-bools \
		-A clippy::if-not-else \
		-A clippy::manual-let-else \
		-A clippy::match-bool \
		-A clippy::match-same-arms \
		-A clippy::missing-errors-doc \
		-A clippy::missing-panics-doc \
		-A clippy::module-name-repetitions \
		-A clippy::must-use-candidate \
		-A clippy::needless-pass-by-value \
		-A clippy::similar-names \
		-A clippy::single-match-else \
		-A clippy::struct-excessive-bools \
		-A clippy::too-many-lines \
		-A clippy::unnecessary-wraps \
		-A clippy::unused-self \
		-A clippy::used-underscore-binding


format-rust:
	cargo fmt --version
	cargo fmt --all
	cargo clippy --version
	cargo clippy --tests --fix --allow-dirty -- \
		-D warnings \
		-W clippy::pedantic \
		-W clippy::dbg_macro \
		-W clippy::print_stdout \
		-A clippy::cast-possible-truncation \
		-A clippy::cast-possible-wrap \
		-A clippy::cast-precision-loss \
		-A clippy::cast-sign-loss \
		-A clippy::doc-markdown \
		-A clippy::float-cmp \
		-A clippy::fn-params-excessive-bools \
		-A clippy::if-not-else \
		-A clippy::manual-let-else \
		-A clippy::match-bool \
		-A clippy::match-same-arms \
		-A clippy::missing-errors-doc \
		-A clippy::missing-panics-doc \
		-A clippy::module-name-repetitions \
		-A clippy::must-use-candidate \
		-A clippy::needless-pass-by-value \
		-A clippy::similar-names \
		-A clippy::single-match-else \
		-A clippy::struct-excessive-bools \
		-A clippy::too-many-lines \
		-A clippy::unnecessary-wraps \
		-A clippy::unused-self \
		-A clippy::used-underscore-binding
