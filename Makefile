

clean: ## Delete generated byte code
	@find . -type f -name '*.pyc' -delete
	@find . -type f -path '*/__pycache__/*' -delete
	@coverage erase
	@rm -rf coverage
	@rm -rf .mypy_cache

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

install-requirements-dev:
	pip install -r requirements-dev.txt

update-requirements-dev:
	pip install -U -r requirements-dev.txt

coverage:
	@coverage run -m unittest discover -v

tox:
	@tox

test-report:
	@coverage report
	@coverage html

lint:
	@flake8 --ignore=F403,F405,S101 pytables_mapping
	@mypy -p pytables_mapping
