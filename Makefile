TEST_ARTIFACTS ?= /tmp/coverage

.PHONY: install dev_install install_webui static_type_check pylint style_check test show_version

show_version:
	@python3 -c "import sys; print('Python version:', f'{sys.version_info.major}.{sys.version_info.minor}')"

install:
	python3 -m pip install --upgrade pip setuptools
	python3 -m pip install -r requirements.txt

install_webui: install
	python3 -m pip install -r requirements-webui.txt

dev_install: install
	python3 -m pip install -r dev-requirements.txt

static_type_check:
	python3 -m mypy media_downloader.py utils config_manager.py db.py --ignore-missing-imports

pylint:
	python3 -m pylint media_downloader.py utils config_manager.py db.py -r y

style_check: static_type_check pylint

test:
	python3 -m pytest --cov media_downloader --doctest-modules \
		--cov utils \
		--cov config_manager \
		--cov db \
		--cov-report term-missing \
		--cov-report html:${TEST_ARTIFACTS} \
		--cov-report xml \
		--junit-xml=${TEST_ARTIFACTS}/media-downloader.xml \
		tests/
