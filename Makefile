.PHONY: release release-pypi release-github clean clean-test clean-pyc clean-build help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-testdoc ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@echo "Remove build files (build/, dist/, .egg*, ...)."
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	@echo "Remove python files (*.py[co], __pycache__, ...)."
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-testdoc: ## remove test and coverage artifacts
	@echo "Remove testdoc output files (testdo/_build/html)."
	@rm -rf testdoc/_build/html

release: release-pypi release-github  ## register PyPI and send tags to github

release-pypi:  ## register PyPI
	python setup.py sdist upload

release-github:  ## send tags to github
	git push origin --tags

.PHONY: green green-cov green-single
green:  ## run green test
	@echo "Run green."
	@green tests

green-single:  ## run green with a single process
	@echo "Run green with a single process."
	@green -s 1 tests

green-cov:  # run green and calculate coverage
	@echo "Run green with coverage."
	@green -r -c tests

.PHONY: flake8
flake8:  ## run flake8 syntax check
	flake8 setup.py m2r.py tests

.PHONY: docs
docs:  ## build document
	@sphinx-build -E -W -n -j auto -b html docs docs/_build/html

.PHONY: sphinx
sphinx:  ## run document build server
	@echo "### Sphinx Build Server Start ###"
	@python docs/server.py

.PHONY: check
check:  ## run flake8 and sphinx-build
	@doit

.PHONY: test
test: check green-cov  ## run style check and test
